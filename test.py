from roller.roller import get_company_roles, get_roles
from dbfunctions.dbinsert_roller import insert_roller
import pandas as pd
import json
import time


orgnr = '983609155'
response_dict = get_company_roles(orgnr)

print(type(response_dict))

if response_dict:

    roller = get_roles(response_dict)

    if roller:

        data = [(orgnr, json.dumps(roller))]

        #insert_roller(data)
        print(roller)
        
