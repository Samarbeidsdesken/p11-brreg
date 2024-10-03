
# Functoins for collecting data from API
from enheter.update_enheter import get_updated_companies
from enheter.get_enhet import get_company

# Functions for inserting into database
from dbfunctions.dbinsert_enheter import insert_company
from dbfunctions.dbinsert_forretningsadresse import insert_address
from dbfunctions.dbinsert_orgform import insert_orgform
from dbfunctions.dbinsert_nace import insert_nace
from dbfunctions.dbinsert_employees import insert_employees

# Functions for updating existing records in database
from dbfunctions.dbupdate_enhet_slettet import update_enhet_slettet
from dbfunctions.dbupdate_adresse import update_addresse
from dbfunctions.dbupdate_orgform import update_orgform
from dbfunctions.dbupdate_nace import update_nace
from dbfunctions.dbupdate_employees import update_employees


# Functions for selecting data from database
from dbfunctions.dbselect_address import select_address
from dbfunctions.dbselect_orgform import select_orgform
from dbfunctions.dbselect_employees import select_employees
from dbfunctions.dbselect_nace import select_nace

# Toolbox functions
from toolbox import toolbox

# Others
import pandas as pd
from datetime import datetime

# Get companies where there has been changes. 
updated_orgs = get_updated_companies()



# Collect the companies where there has been changes
if updated_orgs:
    updates = {}
    for elem in updated_orgs['_embedded']['oppdaterteEnheter']:
        if elem['endringstype'] in updates.keys():
            updates[elem['endringstype']].append(elem['organisasjonsnummer'])
        else:
            updates[elem['endringstype']] = [elem['organisasjonsnummer']]

    
    # Loop through all new companies, and insert the 
    # data to the database
    if 'Ny' in updates.keys():
        for ny in updates['Ny']:

            dictdata = get_company(ny)

            enhet = (
                dictdata['organisasjonsnummer'],
                dictdata['navn'],
                dictdata['registreringsdatoEnhetsregisteret'],
                dictdata['stiftelsesdato'],
                dictdata['maalform'],
                dictdata['registrertIFrivillighetsregisteret'],
                dictdata['registrertIMvaRegisteret'],
                dictdata['registrertIForetaksregisteret']
            )

            insert_company([enhet])

            forretningsadresse = toolbox.parse_address(dictdata)

            insert_address([forretningsadresse])

            orgform = (
                dictdata['organisasjonsnummer'],
                dictdata['organisasjonsform']['kode'],
            )

            insert_orgform([orgform])

    # Loop through all deleted companies, and set is_active as false. 
    if 'Sletting' in updates.keys():
        for orgnr in updates['Sletting']:
            update_enhet_slettet(orgnr)

    # Loop through all companies where there has been changes. The code 
    # does not record all types of changes. Only changes in address and 
    # company code

    if 'Endring' in updates.keys():
        for orgnr in updates['Endring']:
            """
            GET THE ADDRESS OF CURRENT COMPANY AND CHECK IF IT IS THE SAME AS THE REGISTERED ONE
            """
            registered_address = select_address(orgnr)
            
            dictdata = get_company(orgnr)
            
            print(dictdata)
            
            new_address = toolbox.parse_address(dictdata)

            if registered_address != new_address:
                end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                
                #update_addresse((end_date, orgnr))
                #insert_address([new_address])
                

            """
            GET THE COMPANY CODE OF THE CURRENT COMPANY AND CHECK IF ITS THE SAME
            """

            registered_orgform = select_orgform(orgnr)
            new_orgform = (
                dictdata['organisasjonsnummer'],
                dictdata['organisasjonsform']['kode'],
            )

            if registered_orgform != new_orgform:
                end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                
                #update_orgform((end_date, orgnr))
                #insert_orgform([new_orgform])
                
            """
            GET THE NACE CODE OF THE CURRENT COMAPMY AND CHECK IF ITS THE SAME
            """
            
            registered_nace = select_nace(orgnr)
            new_nace = (
                dictdata['organisasjonsnummer'],
                dictdata['naeringskode1']['kode']
            )

            if registered_nace != new_nace:
                end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                
                #update_nace((end_date, orgnr))
                #insert_nace([new_orgform])
                
            """
            GET NUMBER OF EMPLOYEES AND CHECK IF ITS THE SAME
            """
            
            registered_employees = select_employees(orgnr)
            new_employees = (
                dictdata['organisasjonsnummer'],
                dictdata['employees']
            )

            if registered_employees != new_employees:
                end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                
                #update_employees((end_date, orgnr))
                #insert_employees([new_orgform])