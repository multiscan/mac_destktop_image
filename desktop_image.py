#!/usr/bin/env python3

# Attempt to go directly into the sqlite db as in 
# https://stackoverflow.com/questions/33533304/change-scaling-for-all-desktop-backgrounds-on-mac-via-a-script

import glob
import os
from pathlib import Path
import random
import sqlite3
from subprocess import run
import sys
from ruamel.yaml import YAML

CONFIG_PATH = Path(sys.argv[0]).with_suffix('.yml')
CONFIG = YAML(typ='safe').load(CONFIG_PATH)

SCALINGS={
  "fill": 1,
  "tile": 2,
  "center": 3,
  "best": 4,
  "fit": 5,
}

COLORS={
  "black": [0.0, 0.0, 0.0],
  "white": [1.0, 1.0, 1.0],
  "grey": [0.5, 0.5, 0.5],
  "dark": [0.2, 0.2, 0.2],
  "brown": [0.30, 0.7, 0.15],
  "green": [0.18, 0.24, 0.15],
}

def weighted_choice(choices):
  total = sum(c["weight"] for c in choices)
  r = random.uniform(0, total)
  upto = 0
  for c in choices:
    w = c["weight"]
    upto += w
    if upto >= r:
      return c
  assert False, "Shouldn't get here"

# --------------------------------------------------------------------- main
dirs=[]
for d in CONFIG["dirs"]:
  m = CONFIG["defaults"].copy()
  m.update(d)
  if (not os.path.isabs(m["dir"])):
    m["dir"] = CONFIG["base"] + m["dir"]
  dirs.append(m)

random.seed()

# test weighted_choice
# for i in range(0, 100):
#   d = weighted_choice(CONFIG["dirs"])["dir"]
#   print(d)

dd = weighted_choice(dirs)
# dd = {"dir": "Test", "scaling": "best", "bgcolor": "black"}
d = dd["dir"]
ff=glob.glob(d + "/*.jpg") + glob.glob(d + "/*.png")
f=random.sample(ff, 1)[0]
bf=os.path.basename(f)
s=SCALINGS[dd["scaling"]]
c=COLORS[dd["bgcolor"]]

dbpath = str( Path.home() / Path('Library/Application Support/Dock/desktoppicture.db'))

# print("directory: %s" % d)
# print("basename:  %s" % bf)
# print("scaling:   %s" % dd["scaling"])
# print("bgcolor:   %4.2f, %4.2f, %4.2f" % (c[0], c[1],  c[2]))
# print("dbpath:    %s" % dbpath)

# Preference key vs meaning:
#  1: Image path
#  2: Scaling method (Fill Screen (1), Tile (2), Center (3), Stretch to Fill Screen (4), Fit to Screen (5))
#  3: Fill color
#  4: Fill color
#  5: Fill color
#  9: Enable automatic changing
# 10: Directory path to images
# 11: Image changing interval
# 12: Random order
# 16: Current image (used when automatic changing is enabled)

conn = sqlite3.connect(dbpath)
curs = conn.cursor()

curs.executescript('''
  DELETE FROM data;
  DELETE FROM displays;
  DELETE FROM pictures;
  DELETE FROM preferences;
  DELETE FROM prefs;
  DELETE FROM spaces;
  INSERT INTO pictures (space_id, display_id) VALUES (null, null);
''')
conn.commit()
curs.execute("INSERT INTO data (value) VALUES ('%s')" % f)     #  1 Image path      (option key  1)
curs.execute("INSERT INTO data (value) VALUES (%d)" % s)       #  2 Scaling         (option key  2)
curs.execute("INSERT INTO data (value) VALUES (%4.2f)" % c[0]) #  3 Color Red       (option key  3)
curs.execute("INSERT INTO data (value) VALUES (%4.2f)" % c[1]) #  4 Color Green     (option key  4)
curs.execute("INSERT INTO data (value) VALUES (%4.2f)" % c[2]) #  5 Color Blue      (option key  5)
curs.execute("INSERT INTO data (value) VALUES (0)")            #  6 Auto change     (option key  9)
curs.execute("INSERT INTO data (value) VALUES ('%s')" % d)     #  7 Image dir       (option key 10)
curs.execute("INSERT INTO data (value) VALUES (30)")           #  8 Change interval (option key 11)
curs.execute("INSERT INTO data (value) VALUES (0)")            #  9 Random order    (option key 12)
curs.execute("INSERT INTO data (value) VALUES ('%s')" % bf)    # 10 Current image   (option key 16)
conn.commit()
curs.executescript('''
  INSERT INTO preferences (key, data_id, picture_id) VALUES (1, 1, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (2, 2, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (3, 3, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (4, 4, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (5, 5, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (9, 6, 1);
  INSERT INTO preferences (key, data_id, picture_id) VALUES (12, 9, 1);
''')
conn.commit()

# TODO: find a way to avoid this!!
run(["killall", "Dock"])
