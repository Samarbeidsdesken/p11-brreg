from enheter.get_enhet import get_company
from roller.roller import get_company_roles, get_roles
from dbfunctions.dbinsert_roller import insert_roller
import pandas as pd
import json
import time

from dbfunctions.dbselect_employees import select_employees

orgnr = '928149838'

company = get_company(orgnr)

print(company)

"""

response_dict = get_company_roles(orgnr)

print(response_dict)

if response_dict:

    roller = get_roles(response_dict)

    if roller:

        data = [(orgnr, json.dumps(roller))]

        #insert_roller(data)
        #print(roller)
   
   
"""     
"""

employees = select_employees('983609155')
print(employees)
"""