import roller
from dbfunctions.dbinsert_roller import insert_roller
import pandas as pd
import json
import time

enheter = pd.read_csv('alle_enheter_110924', delimiter=',')


# iterate through specific columns of the dataframe
counter = 0


start_time = time.time()

for index, row in enheter.loc[:, ['organisasjonsnummer', 'organisasjonsform.kode']].iterrows():

    if row['organisasjonsform.kode'] != 'ENK':
        response_dict = roller.get_company_roles(
            row['organisasjonsnummer'].astype(str)
        )

    if response_dict:
        enhet_roller = roller.get_roles(response_dict)

        if enhet_roller:

            data = [(row['organisasjonsnummer'].astype(
                str), json.dumps(enhet_roller))]

            insert_roller(data)

            counter += 1

    if counter > 1000:
        break

end_time = time.time()

# Calculate the duration
elapsed_time = end_time - start_time

print(f"The for loop took {elapsed_time:.6f} seconds to run.")
