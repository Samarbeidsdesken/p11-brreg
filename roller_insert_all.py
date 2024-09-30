

from dbfunctions.dbselect_all_orgs import select_orgs
from roller import roller
from dbfunctions.dbinsert_roller import insert_roller
import time
import json
import concurrent.futures

all_orgs = select_orgs()

start_time = time.time()

# Define a function to handle each org's processing


def process_org(org):
    response_dict = roller.get_company_roles(org)

    if response_dict:
        enhet_roller = roller.get_roles(response_dict)

        if enhet_roller:
            data = [(org, json.dumps(enhet_roller))]
            insert_roller(data)


# Multithreading setup
def process_all_orgs_multithreaded(all_orgs, max_workers=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit each organization to the pool for processing
        futures = [executor.submit(process_org, org) for org in all_orgs]

        # Optionally, wait for all to complete
        concurrent.futures.wait(futures)


"""
for org in all_orgs:

    response_dict = roller.get_company_roles(org)

    if response_dict:
        enhet_roller = roller.get_roles(response_dict)

        if enhet_roller:

            data = [(org, json.dumps(enhet_roller))]

            insert_roller(data)
"""

# Call the multithreaded function
process_all_orgs_multithreaded(all_orgs, max_workers=10)

end_time = time.time()

# Calculate the duration
elapsed_time = end_time - start_time

print(elapsed_time)
