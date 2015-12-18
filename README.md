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

#Installation
##Linux (Ubuntu/Mint)
_If you are running a distro other than Ubuntu the only thing that should change here is your commands for retreiving psycopg2's dependencies from your package manager_


Install python3 and psycopg2's dependencies:

`sudo apt-get install python3 libpq-dev python-dev`

Install pip if you do not already have it

`sudo apt-get install python3-pip`

Install `psycopg2`, our PostgreSQL driver -- cloning and running via python3 should work after this step.

`pip3 install psycopg2`

Clone down the repo 

`cd /usr/local/lib` <- Change this to wherever you'd like the code to live

`sudo git clone https://github.com/ByzantineFailure/Pyxtools.git`

Configure (see below)

(Optional) Set up a symlink in `/usr/local/bin` -- Only do if you did above into `/usr/local/lib`

`cd /usr/local/bin`

`ln -s /usr/local/lib/Pyxtools/pyxtools pyxtools`

##Mac OS X
1.  Install python3
2.  Install psycopg2
3.  Clone down repo
4.  Configure (see below)
5.  (Optional) Add a symlink to `/usr/local/bin` to put the repo on your PATH

##Windows
1.  [Install python3](https://www.python.org/downloads/windows/)
2.  [Install psycopg2](http://www.stickpeople.com/projects/python/win-psycopg/)
3.  Clone down the repo
4.  Configure (see below)
5.  (Optional) Put the repo on your `%PATH%` ([this howto might work, YMMV I have not done it](http://www.windows-commandline.com/set-path-command-line/))
  
#Configuration
In the repo's root, open `lib/config.py` and set the `dbConnString` variable to a connection string which will connect you to your PretendYoureXyzzy instance's postgreSQL database as the correct user.  ([An example](https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL#Connect_to_Postgres))
