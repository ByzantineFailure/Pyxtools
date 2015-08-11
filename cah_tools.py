from config import *
import psycopg2
import psycopg2.extras
import json
import time
import sys

config = getConfig();

connString = config['connString'];

def backUpCardSet(setId):
        try:
                conn = psycopg2.connect(connString);
        except:
                print("Unable to connect to database");
                
        card_set = getCardSet (setId, conn);

        encoded = json.dumps(card_set, separators=(',',':'));

        filename = card_set['name'] + " backup " + time.strftime("%m-%d-%y") + " " + time.strftime("%H %M %S") + ".dat";

        backup_file = open(filename, 'w');
        backup_file.write(encoded);
        backup_file.close();
                             
        conn.close();

def getCardSet(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        card_set_query = "SELECT active, name, base_deck, description, weight FROM card_set WHERE id = %s ;";

        try:
                cur.execute(card_set_query, (str(setId), ));
        except:
                print("Couldn't get card set for set id " + str(setId) + "!");
                return;
        
        card_set = dict(cur.fetchall()[0]);
        card_set['black_cards'] = getCardSetBlackCards(setId, conn);
        card_set['white_cards'] = getCardSetWhiteCards(setId, conn);
        print(card_set);        
        return card_set;

def getCardSetWhiteCards(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        card_set_query = "SELECT * FROM card_set_white_card WHERE card_set_id = %s ;";
        white_card_query = "SELECT text, watermark FROM white_cards WHERE id = ANY (%s);";

        try:
                cur.execute(card_set_query, (str(setId), ));
        except:
                print("Couldn't get card set white card ids for set id " + str(setId) + "!");
        
        rows = cur.fetchall();

        white_card_ids = [value['white_card_id'] for value in rows]

        try:
                cur.execute(white_card_query, (white_card_ids, ));
        except:
                print("Some error in getting white cards");                

        rows = cur.fetchall();

        retArray = [];
        
        for value in rows:
                retArray.append({ 'text' : value[0], 'watermark' : value[1]});        

        cur.close();
        
        return retArray;

def getCardSetBlackCards(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        card_set_query = "SELECT * FROM card_set_black_card WHERE card_set_id = %s ;";
        black_card_query = "SELECT text, draw, pick, watermark FROM black_cards WHERE id = ANY (%s);";

        try:
                cur.execute(card_set_query, (str(setId), ));
        except:
                print("Couldn't get card set black card ids for set id " + str(setId) + "!");
        
        rows = cur.fetchall();

        black_card_ids = [value['black_card_id'] for value in rows];

        
        try:
                cur.execute(black_card_query, (black_card_ids, ));
        except:
                print("Some error in getting black cards");                

        rows = cur.fetchall();
        
        cur.close();

        retArray = [];

        for value in rows:
                retArray.append({ 'text' : value[0], 'draw' : value[1], 'pick' : value[2],
                          'watermark' : value[3] });
        
        return retArray;

def restoreCardSet(filename):
        file = open(filename, 'r');
        set_json = file.read();
        file.close();

        card_set = json.loads(set_json);

        try:
                conn = psycopg2.connect(connString);
        except:
                print("Unable to connect to database");
        
        try:
                card_set_id = insertCardSetRecord(card_set, conn);
                insertBlackCards(card_set['black_cards'], card_set_id, conn);
                insertWhiteCards(card_set['white_cards'], card_set_id, conn);
        except:
                print("Error inserting card set.  Rolling everything back...");
                print("Error was: \n{}".format(sys.exc_info()[2].format_exception()));
                conn.rollback();

        conn.commit();
        conn.close();

def insertCardSetRecord(card_set, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        card_set_query = "INSERT INTO card_set (id, active, name, base_deck, description, weight) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;";
        max_id_query = "SELECT MAX(id) FROM card_set";

        cur.execute(max_id_query);
        
        max_id = cur.fetchone()[0];

        if(max_id is None):
                max_id = 0;

        max_id += 1;
        
        print(cur.mogrify(card_set_query, (max_id, card_set['active'], card_set['name'], card_set['base_deck'], card_set['description'], card_set['weight'])));
        
        cur.execute(card_set_query, (max_id, card_set['active'], card_set['name'], card_set['base_deck'], card_set['description'], card_set['weight']));
        set_id = cur.fetchone()[0];

        cur.close();
        
        return set_id;

def insertBlackCards(black_cards, card_set_id, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        insert_base_query = "INSERT INTO black_cards (text, draw, pick, watermark) VALUES (%s, %s, %s, %s) RETURNING id;";
        all_ids_query = "SELECT id FROM black_cards WHERE id > %s ;";
        insert_set_query = "INSERT INTO card_set_black_card (card_set_id, black_card_id) VALUES (%s, %s);";
        
        for card in black_cards:
           card_query = cur.mogrify(insert_base_query, (card['text'], card['draw'], card['pick'], card['watermark']));
           print(card_query);
           cur.execute(card_query);
           card_id = cur.fetchone()[0];
           card_set_query = cur.mogrify(insert_set_query, (card_set_id, card_id));
           print(card_set_query);
           cur.execute(card_set_query);

        return;

def insertWhiteCards(white_cards, card_set_id, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
        insert_base_query = "INSERT INTO white_cards (text, watermark) VALUES (%s, %s) RETURNING id;";
        insert_set_query = "INSERT INTO card_set_white_card (card_set_id, white_card_id) VALUES (%s, %s);";
	
        for card in white_cards:
            card_query = cur.mogrify(insert_base_query, (card['text'], card['watermark']));
            print(card_query);
            cur.execute(card_query);
            card_id = cur.fetchone()[0];
            card_set_query = cur.mogrify(insert_set_query, (card_set_id, card_id));
            print(card_set_query);
            cur.execute(card_set_query);
                
        return;

restoreCardSet("dmc_bk.json");
