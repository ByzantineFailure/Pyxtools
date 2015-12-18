#!/usr/bin/env python3
import argparse
import sys
from args import getArgs
import db

args = getArgs().parse_args()

conn = db.getConnection()

def exitWithMessage(message):
    print(message);
    conn.close();
    sys.exit(1);

def createBlackCard():
    card = dict()
    if args.text == None or args.text == '':
        exitWithMessage('Specify card text for inserted black card (-t)')
    card['text'] = args.text    

    if args.draw < 0:
        exitWithMessage('Draw cannot be less than zero (-d)')
    card['draw'] = args.draw

    if args.pick <= 0:
        exitWithMessage('Pick cannot be less than or equal to zero (-p)')
    card['pick'] = args.pick

    if args.watermark == '' or args.watermark == None:
        exitWithMessage('Watermark cannot be blank (--watermark)')
    card['watermark'] = args.watermark

    return card

def createWhiteCard():
    card = dict()
    if args.text == None or args.text == '':
        exitWithMessage('Specify card text for inserted white card (-t)')
    card['text'] = args.text

    if args.watermark == '':
        exitWithMessage('Cannot have blank watermark (--watermark)')
    card['watermark'] = args.watermark

    return card

def doInsert():
    card = None
    if args.white:
        card = createWhiteCard()
    else:
        card = createBlackCard()

    print('Are you sure you want to insert ' + ('white' if args.white else 'black') + ' card to card set ' + str(args.cardset) + '?')
    print(str(card))
    choice = input('Y/N? ')
    if choice != 'Y' and choice != 'y':
        print('Exiting...')
        conn.close()
        sys.exit(0)

    if args.white:
        db.insertWhiteCards([card], args.cardset, conn)
    else:
        db.insertBlackCards([card], args.cardset, conn)
    
    conn.commit()
    print('Inserted')

def doDelete():
    print('Not yet implemented!')

def doExport():
    db.backUpCardSet(args.cardset, args.filename)
    print('Export successful')

def doImport():
    db.restoreCardSet(args.filename)
    print('Import successful')

def doCardsets():
    sets = db.getCardSetList(conn)
    for cardset in sets:
        print(str(cardset['id']) + ',' + cardset['name'] + ',' + str(cardset['active']))
    

#Because python has no switch
commands = {
    'insert': lambda: doInsert(),
    'delete': lambda: doDelete(),
    'export': lambda: doExport(),
    'import': lambda: doImport(),
    'cardsets': lambda: doCardsets(),
}[args.command]()

conn.close();
