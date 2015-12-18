import argparse
from lib import config

config = config.getConfig()

def getArgs():
    parser = argparse.ArgumentParser(description='CLI tools for a PYX database')
    commandparser = parser.add_subparsers(help="Commands", dest='command')
    commandparser.required = True

    #Insert
    insertparser = commandparser.add_parser('insert', help='Insert a card')
    
    icardtype = insertparser.add_subparsers(help='Card colors', dest='cardcolor')
    
    iwhitecard = icardtype.add_parser('white', help='Insert a white card')
    iwhitecard.add_argument('-t', '--text', type=str, help='Card text', required = True)
    iwhitecard.add_argument('-w', '--watermark', type=str, default=config['defaultWatermark'], help='Card watermark.  Defaults to ' + config['defaultWatermark'])
    iwhitecard.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set ID to insert the card into.  Defaults to ' + str(config['defaultCardSet']))
    
    iblackcard = icardtype.add_parser('black', help='Insert a black card')
    iblackcard.add_argument('-t', '--text', type=str, help='Card text', required = True)
    iblackcard.add_argument('-p', '--pick', type=int, default=1, help='Number of blanks on the card/cards to pick.  Defaults to one')
    iblackcard.add_argument('-d', '--draw', type=int, default=0, help='Number of cards to draw before playing.  Defaults to zero')
    iblackcard.add_argument('-w', '--watermark', type=str, default=config['defaultWatermark'], help='Card watermark.  Defaults to ' + config['defaultWatermark'])
    iblackcard.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set ID to insert the card into.  Defaults to ' + str(config['defaultCardSet']))

    #Delete
    deleteparser = commandparser.add_parser('delete', help='Delete a card by id')
    
    dcardtype = deleteparser.add_subparsers(help='Card colors', dest='cardcolor')

    dwhitecard = dcardtype.add_parser('white', help='Delete a white card')
    dwhitecard.add_argument('-i', '--id', type=int, help='Id of card to delete', required = True)
    
    dblackcard = dcardtype.add_parser('black', help='Delete a black card')
    dblackcard.add_argument('-i', '--id', type=int, help='Id of card to delete', required = True)

    #Import
    importparser = commandparser.add_parser('import', help='Import a card set to JSON')
    importparser.add_argument('-f', '--filename', type=str, help='File to import', required = True)
    importparser.add_argument('-s', '--cardset', type=int, help='UNIMPLEMENTED Cardset id to insert as (fails if already exists)')

    #Export
    exportparser = commandparser.add_parser('export', help='Export a card set to JSON (by id)')
    exportparser.add_argument('-f', '--filename', type=str, help='File to export to', required = True)
    exportparser.add_argument('-s', '--cardset', type=int, help='ID of card set to export (Default defined as ' + str(config['defaultCardSet']), required = True)

    #Getsets
    setsparser = commandparser.add_parser('cardsets', help='List available cardsets (grep recommended)')
    cscardcolor = setsparser.add_subparsers(help='Card colors', dest='cardcolor')
    
    cswhitecard = cscardcolor.add_parser('white', help='Get white cards from a card set')
    cswhitecard.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set to retreive cards for.  Defaults to ' + str(config['defaultCardSet']), required = True)
    
    csblackcard = cscardcolor.add_parser('black', help='Get black cards from a card set')
    csblackcard.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set to retreive cards for.  Defaults to ' + str(config['defaultCardSet']), required = True)

    return parser

