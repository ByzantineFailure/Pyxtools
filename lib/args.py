import argparse
import enum
from lib import config

config = config.getConfig()

class ImportDuplicateBehavior(enum.Enum):
    fail = 1
    askAndFail = 2
    askAndSkip = 3
    link = 4

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
    importparser.add_argument('-s', '--cardset', type=int, help='Cardset id to insert as (fails if already exists)', required = True)

    duplicateBehavior = importparser.add_mutually_exclusive_group()
    duplicateBehavior.add_argument('--failOnDuplicate', dest='duplicateBehavior', action='store_const', const=ImportDuplicateBehavior.fail.value, help="Fail on duplicate cards.  Default behavior")
    duplicateBehavior.add_argument('--askAndFailOnDuplicate', dest='duplicateBehavior', action='store_const', const=ImportDuplicateBehavior.askAndFail.value, help="Ask whether or not to link when a duplicate is found. Fails operation if any card is denied")
    duplicateBehavior.add_argument('--askAndSkipOnDuplicate', dest='duplicateBehavior', action='store_const', const=ImportDuplicateBehavior.askAndSkip.value, help="Ask whether or not to link when a duplicate is found.  Skips rejected cards")
    duplicateBehavior.add_argument('--linkOnDuplicate', dest='duplicateBehavior', action='store_const', const=ImportDuplicateBehavior.link.value, help="Automatically link the existing card on existing duplicate")

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

