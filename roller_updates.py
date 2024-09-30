
from roller import update_roller
from roller import roller
from dbfunctions.dbinsert_roller import insert_roller
from dbfunctions.dbupdate_roller import insert_roller_update
# import matplotlib.pyplot as plt
import json
from datetime import datetime


updated_orgs = update_roller.get_updated_roles()


for org in updated_orgs:
    # print(org)
    orgnr = org['data']['organisasjonsnummer']

    response_dict = roller.get_company_roles(orgnr)

    if response_dict:
        enhet_roller = roller.get_roles(response_dict)

        if enhet_roller:

            data = [(orgnr, json.dumps(enhet_roller))]

            try:
                end_time = datetime.strptime(
                    org['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                insert_roller_update((end_time, orgnr))
                insert_roller(data)
            except:
                print(f'Failed to update {orgnr}')
