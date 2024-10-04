
# Functoins for collecting data from API
from enheter.update_enheter import get_updated_companies
from enheter.get_enhet import get_company

# Functions for inserting into database
from dbfunctions.dbinsert_enheter import insert_company
from dbfunctions.dbinsert_forretningsadresse import insert_address
from dbfunctions.dbinsert_orgform import insert_orgform
from dbfunctions.dbinsert_nace import insert_nace
from dbfunctions.dbinsert_employees import insert_employees
from dbfunctions.dbupdate_enhet_konkurs import update_enhet_konkurs

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
from dbfunctions.dbselect_enheter_maxid import select_enheter_maxid

# Toolbox functions
from toolbox import toolbox

# Others
import pandas as pd
from datetime import datetime

enheter_maxid = select_enheter_maxid()

# Get companies where there has been changes. 
updated_orgs = get_updated_companies(enheter_maxid)



# Collect the companies where there has been changes
if updated_orgs:
    updates = {}
    oppdateringsid = {}
    for elem in updated_orgs['_embedded']['oppdaterteEnheter']:
        if elem['endringstype'] in updates.keys():
            updates[elem['endringstype']].append(elem['organisasjonsnummer'])
            
        else:
            updates[elem['endringstype']] = [elem['organisasjonsnummer']]

        oppdateringsid[elem['organisasjonsnummer']] = elem['oppdateringsid']
    
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
                None, #dictdata['konkurs'],
                None #dictdata['konkursdato']
            )

            #insert_company([enhet])

            forretningsadresse = toolbox.parse_address(dictdata)

            #insert_address([forretningsadresse], oppdateringsid[ny])

            orgform = (
                dictdata['organisasjonsnummer'],
                dictdata['organisasjonsform']['kode'],
            )

            #insert_orgform([orgform], oppdateringsid[ny])
            
            nace = (
                dictdata['organisasjonsnummer'],
                dictdata['naeringskode1']['kode']
            )
            
            #insert_nace(nace)
            
            if dictdata['harRegistrertAntallAnsatte'] == True:
                
                employees = (
                    dictdata['organisasjonsnummer'],
                    dictdata['employees']
                )

                #insert_employees([employees], oppdateringsid[ny])
                
           
    # Loop through all deleted companies, and set is_active as false. 
    if 'Sletting' in updates.keys():
        for orgnr in updates['Sletting']:
            pass
            #update_enhet_slettet(orgnr)

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
            
            new_address = toolbox.parse_address(dictdata)

            if registered_address != new_address:
                end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                
                update_addresse((end_date, orgnr))
                insert_address([new_address], oppdateringsid[orgnr])
                

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
                
                update_orgform((end_date, orgnr))
                insert_orgform([new_orgform], oppdateringsid[orgnr])
                
            """
            GET THE NACE CODE OF THE CURRENT COMPANY AND CHECK IF ITS THE SAME
            """
            
            if 'naeringskode1' in dictdata.keys():
            
                registered_nace = select_nace(orgnr)
                
                new_nace = (
                    dictdata['organisasjonsnummer'],
                    dictdata['naeringskode1']['kode']
                )

                if registered_nace != new_nace:
                    end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                    
                    update_nace((end_date, orgnr))
                    insert_nace([new_nace], oppdateringsid[orgnr])
                
            """
            GET NUMBER OF EMPLOYEES AND CHECK IF ITS THE SAME
            """
            
            if dictdata['harRegistrertAntallAnsatte'] == True and 'antallAnsatte' in dictdata.keys():
                
                registered_employees = select_employees(orgnr)
                
                new_employees = (
                    dictdata['organisasjonsnummer'],
                    dictdata['antallAnsatte']
                )

                # Is none if employers are not registered
                if registered_employees:
                    
                    if registered_employees != new_employees:

                        end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
                        
                        update_employees((end_date, orgnr))
                        insert_employees([new_employees], oppdateringsid[orgnr])
                else: 
                    pass
                    insert_employees([new_employees], oppdateringsid[orgnr])
                    
            """
            CHECK BANKRUPTCY
            """
            if dictdata['konkurs'] == True:
                konkurs = (dictdata['konkursdato'], orgnr)
                update_enhet_konkurs(konkurs)
                
                
            
            
            
            