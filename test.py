
# Functions for communicating with brreg API
from roller import update_roller
from roller import roller

# Functions for writing data to database
from dbfunctions.dbinsert_roller import insert_roller
from dbfunctions.dbupdate_roller import insert_roller_update

# Functions for selecting from database
from dbfunctions.dbselect_roller_maxid import select_roller_maxid
from dbfunctions.dbselect_enheter_ids import select_enheter_ids

# Others
import json
from datetime import datetime

maxid = select_enheter_ids(remote = True)

print(maxid)