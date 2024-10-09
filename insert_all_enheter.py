
import pandas as pd
import numpy as np
from dbfunctions.dbinsert_enheter import insert_company
from dbfunctions.dbinsert_forretningsadresse import insert_address
from dbfunctions.dbinsert_orgform import insert_orgform
from dbfunctions.dbinsert_nace import insert_nace
from dbfunctions.dbinsert_employees import insert_employees
from datetime import datetime

import concurrent.futures

# from concurrent.futures import ThreadPoolExecutor, as_completed


df = pd.read_csv('enheter/alle_enheter_091024.csv', delimiter=',', dtype={
                 'forretningsadresse.kommunenummer': object, 'forretningsadresse.postnummer': object})

# Replace empty strings in date columns with NaN (equivalent to NULL)
date_columns = ['registreringsdatoenhetsregisteret', 'stiftelsesdato', 'konkursdato',
                'underAvviklingDato', 'tvangsopplostPgaManglendeDagligLederDato',
                'tvangsopplostPgaManglendeRevisorDato', 'tvangsopplostPgaManglendeRegnskapDato',
                'tvangsopplostPgaMangelfulltStyreDato', 'tvangsavvikletPgaManglendeSlettingDato',
                'vedtektsdato']

# Replace empty date values with NaN
df[date_columns] = df[date_columns].replace("", pd.NA)

df = df.replace({np.nan: None})

pd.options.display.float_format = '{:,.0f}'.format

df.rename(
    columns={
        # 'organisasjonsform.kode': 'organisasjonsform_kode',
        'forretningsadresse.adresse': 'forretningsadresse_adresse',
        'forretningsadresse.postnummer': 'forretningsadresse_postnummer',
        'forretningsadresse.kommunenummer': 'forretningsadresse_kommunenummer',
        'forretningsadresse.land': 'forretningsadresse_land',
        'forretningsadresse.landkode': 'forretningsadresse_landkode',
        'organisasjonsform.kode': 'orgform_kode',
        'naeringskode1.kode': 'naeringskode1',
        'naeringskode2.kode': 'naeringskode2',
        'naeringskode3.kode': 'naeringskode3'
    }, inplace=True)


# --------------------------------- #
# BASIC INFORMATION ABOUT COMPANIES #
# --------------------------------- #

enheter = df[['organisasjonsnummer', 'navn',
              'registreringsdatoenhetsregisteret', 'stiftelsesdato', 'maalform', 'konkurs', 'konkursdato']]

enheter = enheter.replace({np.nan: None})

# ------------ #
# ADDRESS INFO #
# ------------ #

forretningsadresse = df[['organisasjonsnummer', 'forretningsadresse_adresse', 'forretningsadresse_postnummer',
                         'forretningsadresse_kommunenummer', 'forretningsadresse_land', 'forretningsadresse_landkode']]

# forretningsadresse['start_date'] = datetime.today().strftime('%Y-%m-%d')
forretningsadresse = forretningsadresse.replace({np.nan: None})

# ------------------- #
# ORGANISATIONAL CODE #
# ------------------- #

orgform = df[['organisasjonsnummer', 'orgform_kode']]

# ------------- #
# INDUSTRY CODE #
# ------------- #

nace = df[['organisasjonsnummer', 'naeringskode1']]

# --------- #
# EMPLOYEES #
# --------- #

employees_filtered = df[df['harRegistrertAntallAnsatte'] == True]

employees = employees_filtered[['organisasjonsnummer', 'antallAnsatte']]

employees = employees[employees['antallAnsatte'].notna()]


# ------------------ #
# INSERT IN DATABASE #
# ------------------ #

"""
for row in enheter.head(1000).itertuples(name=None, index=False):
    insert_company([row])

for row in forretningsadresse.head(1000).itertuples(name=None, index=False):
    insert_address([row])

for row in orgform.head(1000).itertuples(name=None, index=False):
    insert_orgform([row])

"""
# Define a function to insert each dataset



def insert_dataset(insert_function, dataset):
    for row in dataset.itertuples(name=None, index=False):
        insert_function([row])


# Set up multithreading
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit the tasks to be run in parallel
    future_enheter = executor.submit(
        insert_dataset, insert_company, enheter)
    future_forr_adresse = executor.submit(
        insert_dataset, insert_address, forretningsadresse)
    future_orgform = executor.submit(
        insert_dataset, insert_orgform, orgform)
    future_orgform = executor.submit(
        insert_dataset, insert_nace, nace)
    future_orgform = executor.submit(
        insert_dataset, insert_employees, employees)

    # Optionally, wait for all to finish (this is useful for error handling/logging)
    concurrent.futures.wait(
        [future_enheter, future_forr_adresse, future_orgform])
