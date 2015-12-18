Pyxtools
=======================

A few simple tools to help me administrate the Pretend You're Xyzzy server I administrate for some friends.

Provides functionality for viewing card sets and their cards, adding and deleting cards to and from cardsets, and backing up and restoring cardsets (via a JSON file).

Detailed usage and help is provided via the `-h` flag provided by python's argparse library, but the the basic commands are:

`pyxtools cardsets` - list all cardsets

`pyxtools cardsets white -s CARDSET` - list a cardset's white cards

`pyxtools cardsets black -s CARDSET` - list a cardset's black cards

`pyxtools insert` - insert a card.  See `pyxtools insert -h` for detailed information. 

`pyxtools delete` - delete a card.  See `pyxtools delete -h` for detailed information.

`pyxtools export -s CARDSET -f FILENAME` - export a cardset to a file

`pyxtools import -f FILENAME` - import a cardset from a file

_Requires python3, psycopg2._
