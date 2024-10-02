
# Functions for communicating with brreg API
from roller import update_roller
from roller import roller

# Functions for writing data to database
from dbfunctions.dbinsert_roller import insert_roller
from dbfunctions.dbupdate_roller import insert_roller_update

# Functions for selecting from database
from dbfunctions.dbselect_roller_maxid import select_roller_maxid

# Others
import json
from datetime import datetime

maxid = select_roller_maxid()

# Get companies where the roles have been updated
updated_orgs = update_roller.get_updated_roles(maxid)

# Create a set of unique orgs
# One company can appear multiple times

changes = dict()

# Chreate a dictionary called changes, where 
# each company is key and the change id is added to a list.
# The list of ids is sorted. It is only necessary to 
# collect the latest change (max id)
for org in updated_orgs:    
    orgnr = org['data']['organisasjonsnummer']
    
    if orgnr in changes.keys():
        changes[orgnr].append(int(org['id']))
    else:
        changes[orgnr] = [int(org['id'])]
    #unique_orgs.add(org['data']['organisasjonsnummer'])

# Sorting the lists for each key
for key in changes:
    changes[key].sort()

# Creating a set to store the maximum values
changeids = set()

# Collecting the maximum value from each list and adding it to the set
for key in changes:
    changeids.add(max(changes[key]))
    
print(len(changes))
"""

# Loop through all changes
for org in updated_orgs:
    if int(org['id']) in changeids:
        
        orgnr = org['data']['organisasjonsnummer']
        id = int(org['id'])
        
        # Get the new company roles
        response_dict = roller.get_company_roles(orgnr)

        # If company roles
        if response_dict:
            # parse roles from dict
            enhet_roller = roller.get_roles(response_dict)

            if enhet_roller:
                # make a tuple with orgnr and a json string
                data = [(orgnr, id, json.dumps(enhet_roller))]

                try:
                    end_time = datetime.strptime(
                        org['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    insert_roller_update((end_time, orgnr))
                    insert_roller(data)
                except:
                    print(f'Failed to update {orgnr}')
"""