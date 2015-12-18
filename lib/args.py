import argparse
from lib import config

config = config.getConfig()

def getArgs():
    parser = argparse.ArgumentParser(description='CLI tools for a PYX database')
    commandparser = parser.add_subparsers(help="Commands", dest='command')
    commandparser.required = True

    #Insert
    insertparser = commandparser.add_parser('insert', help='Insert a card')

    icardtypepg = insertparser.add_argument_group(title = 'Card Type')
    icardtype = icardtypepg.add_mutually_exclusive_group(required = True)
    icardtype.add_argument('-w', '--white', action='store_true', help='Insert a white card')
    icardtype.add_argument('-b', '--black', action='store_true', help='Insert a black card')

    cardinfo = insertparser.add_argument_group('Card Information')
    cardinfo.add_argument('-t', '--text', type=str, help='Card text', required = True)
    cardinfo.add_argument('-p', '--pick', type=int, default=1, help='Number of blanks on the card/cards to pick.  Defaults to one')
    cardinfo.add_argument('-d', '--draw', type=int, default=0, help='Number of cards to draw before playing.  Defaults to zero')
    cardinfo.add_argument('-m', '--watermark', type=str, default=config['defaultWatermark'], help='Card watermark.  Defaults to ' + config['defaultWatermark'])
    cardinfo.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set ID to insert the card into.  Defaults to ' + str(config['defaultCardSet']))

    #Delete
    deleteparser = commandparser.add_parser('delete', help='Delete a card (by id) -- Not yet implemented')

    dcardtypepg = deleteparser.add_argument_group(title = 'Card Information')
    dcardtypepg.add_argument('-i', '--id', type=int, help='Id of card to delete', required = True)
    dcardtype = dcardtypepg.add_mutually_exclusive_group(required = True)
    dcardtype.add_argument('-w', '--white', action='store_true', help='Delete a white card')
    dcardtype.add_argument('-b', '--black', action='store_true', help='Delete a black card')

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
    colorparser = setsparser.add_subparsers(help='Card colors', dest='cardcolor')
    
    whiteparser = colorparser.add_parser('white', help='Get white cards from a card set')
    whiteparser.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set to retreive cards for.  Defaults to ' + str(config['defaultCardSet']), required = True)
    
    blackparser = colorparser.add_parser('black', help='Get black cards from a card set')
    blackparser.add_argument('-s', '--cardset', type=int, default=config['defaultCardSet'], help='Card set to retreive cards for.  Defaults to ' + str(config['defaultCardSet']), required = True)

    return parser

