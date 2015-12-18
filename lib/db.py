from lib import config
import psycopg2
import psycopg2.extras
import json
import time
import sys
import traceback

connString = config.getConfig()['connString'];

def getConnection():
    try:
        return psycopg2.connect(connString);
    except:
        print('Unable to connect to database!')

def backUpCardSet(setId, filename, conn):
        card_set = getCardSet (setId, conn);
        
        #Remove Ids which we don't want while backing up to JSON
        for card in card_set['black_cards']:
            card.pop('id', None)
        for card in card_set['white_cards']:
            card.pop('id', None)

        encoded = json.dumps(card_set, separators=(',',':'));

        backup_file = open(filename, 'w');
        backup_file.write(encoded);
        backup_file.close();
                             
def getCardSetList(conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor);
    query = "SELECT id, name, active FROM card_set;";

    try:
        cur.execute(query);
    except:
        print("Couldn't get card sets");
        traceback.print_exc();
        return;

    sets = cur.fetchall()
    return sets

def getCardSet(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        card_set_query = "SELECT active, name, base_deck, description, weight FROM card_set WHERE id = %s ;"
        
        try:
                cur.execute(card_set_query, (str(setId), ))
        except:
                print("Couldn't get card set for set id " + str(setId) + "!")
                return
        
        card_set = dict(cur.fetchall()[0])
        card_set['black_cards'] = getCardSetBlackCards(setId, conn)
        card_set['white_cards'] = getCardSetWhiteCards(setId, conn)
        return card_set;

def getCardSetWhiteCards(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        card_set_query = "SELECT * FROM card_set_white_card WHERE card_set_id = %s ;"
        white_card_query = "SELECT id, text, watermark FROM white_cards WHERE id = ANY (%s);"

        try:
                cur.execute(card_set_query, (str(setId), ))
        except:
                print("Couldn't get card set white card ids for set id " + str(setId) + "!")
        
        rows = cur.fetchall()
        white_card_ids = [value['white_card_id'] for value in rows]

        try:
                cur.execute(white_card_query, (white_card_ids, ))
        except:
                print("Some error in getting white cards");               

        rows = cur.fetchall()
        retArray = []
        
        for value in rows:
            retArray.append({ 'id': value[0], 'text' : value[1], 'watermark' : value[2]})

        cur.close()
        
        return retArray

def getCardSetBlackCards(setId, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        card_set_query = "SELECT * FROM card_set_black_card WHERE card_set_id = %s ;"
        black_card_query = "SELECT id, text, draw, pick, watermark FROM black_cards WHERE id = ANY (%s);"

        try:
                cur.execute(card_set_query, (str(setId), ))
        except:
                print("Couldn't get card set black card ids for set id " + str(setId) + "!")
        
        rows = cur.fetchall()

        black_card_ids = [value['black_card_id'] for value in rows]

        
        try:
                cur.execute(black_card_query, (black_card_ids, ))
        except:
                print("Some error in getting black cards")

        rows = cur.fetchall()
        
        cur.close()

        retArray = []

        for value in rows:
            retArray.append({ 'id' : value[0], 'text' : value[1], 'draw' : value[2], 'pick' : value[3],
                          'watermark' : value[4] })
        
        return retArray

def restoreCardSet(card_set_id, filename, conn):
        file = open(filename, 'r')
        set_json = file.read()
        file.close()

        card_set = json.loads(set_json)
        
        try:
                inserted_set_id = insertCardSetRecord(card_set_id, card_set, conn)
                insertBlackCards(card_set['black_cards'], inserted_set_id, conn)
                insertWhiteCards(card_set['white_cards'], inserted_set_id, conn)
                return card_set_id
        except:
                print("Error inserting card set.  Rolling everything back...")
                traceback.print_exc()
                conn.rollback()
                return -1


def insertCardSetRecord(card_set_id, card_set, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        set_exists_query = "SELECT * FROM card_set WHERE id = %s"
        final_query = None
        inserted_id = -1
        
        set_exists_query = cur.mogrify(set_exists_query, (card_set_id,))
        print(set_exists_query)
        cur.execute(set_exists_query)
        if cur.rowcount > 0:
            raise Exception('Card set with id ' + str(card_set_id) + ' already exists');
        card_set_query = cur.mogrify("INSERT INTO card_set (id, active, name, base_deck, description, weight) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
            (card_set_id, card_set['active'], card_set['name'], card_set['base_deck'], card_set['description'], card_set['weight']))

        print(card_set_query)
        
        cur.execute(card_set_query)
        set_id = cur.fetchone()[0]
        
        cur.close()
        return set_id

def insertBlackCards(black_cards, card_set_id, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        black_card_values = [cur.mogrify('(%s, %s, %s, %s)', (card['text'], card['draw'], card['pick'], card['watermark'])).decode('utf-8') for card in black_cards]
        insert_base_query = 'INSERT INTO black_cards (text, draw, pick, watermark) VALUES ' + ','.join(black_card_values) + ' RETURNING id;'
        print(insert_base_query)

        cur.execute(insert_base_query)
        ids = cur.fetchall()

        id_values = [cur.mogrify('(%s, %s)', (card_set_id, id[0])).decode('utf-8') for id in ids]
        insert_set_query = 'INSERT INTO card_set_black_card (card_set_id, black_card_id) VALUES ' + ','.join(id_values) + ';'
        print(insert_set_query)

        cur.execute(insert_set_query)
        cur.close()
        return

def insertWhiteCards(white_cards, card_set_id, conn):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        white_card_values = ','.join([cur.mogrify('(%s, %s)', (card['text'], card['watermark'])).decode('utf-8') for card in white_cards])
        insert_wc_query = 'INSERT INTO white_cards (text, watermark) VALUES ' + white_card_values + ' RETURNING id;'
        print(insert_wc_query)

        cur.execute(insert_wc_query)
        wc_ids = cur.fetchall()
        
        insert_wccs_query = 'INSERT INTO card_set_white_card (card_set_id, white_card_id) VALUES ';
        id_values = ','.join([cur.mogrify('(%s, %s)', (card_set_id, id[0])).decode('utf-8') for id in wc_ids])
        insert_wccs_query = insert_wccs_query + id_values + ';'
        print(insert_wccs_query)

        cur.execute(insert_wccs_query)
        cur.close()
        return

def deleteWhiteCard(white_card_id, conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    delete_cswc_query = "DELETE FROM card_set_white_card WHERE white_card_id = %s;";
    delete_wc_query = "DELETE FROM white_cards WHERE id = %s;"

    mog_cswc_query = cur.mogrify(delete_cswc_query, (white_card_id,))
    mog_wc_query = cur.mogrify(delete_wc_query, (white_card_id,))
    try:
        print(mog_cswc_query)
        cur.execute(mog_cswc_query)
        print(mog_wc_query)
        cur.execute(mog_wc_query)
        cur.close()
    except:
        print('Error deleting white card')
        print(traceback.format_exception())

def deleteBlackCard(black_card_id, conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    delete_csbc_query = "DELETE FROM card_set_black_card WHERE black_card_id = %s;"
    delete_bc_query = "DELETE FROM black_cards WHERE id = %s;"

    mog_csbc_query = cur.mogrify(delete_csbc_query, (black_card_id,))
    mog_bc_query = cur.mogrify(delete_bc_query, (black_card_id,))
    try:
        print(mog_csbc_query)
        cur.execute(mog_csbc_query)
        print(mog_bc_query)
        cur.execute(mog_bc_query)
        cur.close()
    except:
        print('Error deleting black card')
        print(traceback.format_exception())

