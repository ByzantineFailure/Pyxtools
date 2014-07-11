from config import *
import psycopg2
import psycopg2.extras
import json
import time

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

backUpCardSet(1151);

