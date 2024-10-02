
# Functions for communicating with brreg API
from roller import update_roller
from roller import roller

# Functions for writing data to database
from dbfunctions.dbinsert_roller import insert_roller
from dbfunctions.dbupdate_roller import insert_roller_update

# Others
import json
from datetime import datetime

# Get companies where the roles have been updated
updated_orgs = update_roller.get_updated_roles()



# Loop through all 
for org in updated_orgs:
    print(org)
    orgnr = org['data']['organisasjonsnummer']
    id = org['data']['id']
    
    
    
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
                #insert_roller_update((end_time, orgnr))
                #insert_roller(data)
            except:
                print(f'Failed to update {orgnr}')
