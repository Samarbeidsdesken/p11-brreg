from enheter.update_enheter import get_updated_companies
from enheter.get_enhet import get_company
from dbfunctions.dbinsert_enheter import insert_company
from dbfunctions.dbinsert_forretningsadresse import insert_address
from dbfunctions.dbinsert_orgform import insert_orgform

from dbfunctions.dbupdate_enhet_slettet import update_enhet_slettet

from dbfunctions.dbselect_address import select_address
from dbfunctions.dbselect_orgform import select_orgform

from dbfunctions.dbupdate_adresse import update_addresse
from dbfunctions.dbupdate_orgform import update_orgform

from enheter.get_enhet import get_company
import pandas as pd
from datetime import datetime

updated_orgs = get_updated_companies()


if updated_orgs:
    updates = {}
    for elem in updated_orgs['_embedded']['oppdaterteEnheter']:
        if elem['endringstype'] in updates.keys():
            updates[elem['endringstype']].append(elem['organisasjonsnummer'])
        else:
            updates[elem['endringstype']] = [elem['organisasjonsnummer']]


data = []


def parse_address(dictdata):
    forretningsadresse_adresse = ''
    if 'forretningsadresse' in dictdata and 'adresse' in dictdata['forretningsadresse']:
        if isinstance(dictdata['forretningsadresse']['adresse'], list):
            forretningsadresse_adresse = ', '.join(
                dictdata['forretningsadresse']['adresse'])
        else:
            forretningsadresse_adresse = str(
                dictdata['forretningsadresse']['adresse'])

    mytuple = (
        dictdata['organisasjonsnummer'],
        forretningsadresse_adresse,
        dictdata['forretningsadresse']['postnummer'],
        dictdata['forretningsadresse']['kommunenummer'],
        dictdata['forretningsadresse']['land'],
        dictdata['forretningsadresse']['landkode']
    )
    mytuple_updated = tuple(
        None if item == '' else item for item in mytuple)

    return mytuple_updated


if 'Ny' in updates.keys():
    for ny in updates['Ny']:
        dictdata = get_company(ny)

        enhet = (
            dictdata['organisasjonsnummer'],
            dictdata['navn'],
            dictdata['registreringsdatoEnhetsregisteret'],
            dictdata['stiftelsesdato'],
            dictdata['maalform']
        )

        insert_company([enhet])

        forretningsadresse = parse_address(dictdata)

        insert_address([forretningsadresse])

        orgform = (
            dictdata['organisasjonsnummer'],
            dictdata['organisasjonsform']['kode'],
        )

        insert_orgform([orgform])

if 'Sletting' in updates.keys():
    for orgnr in updates['Sletting']:
        update_enhet_slettet(org)


if 'Endring' in updates.keys():
    for orgnr in updates['Endring']:

        """
        GET THE ADDRESS OF CURRENT COMPANY AND CHECK IF IT IS THE SAME AS THE REGISTERED ONE
        """
        registered_address = select_address(orgnr)
        dictdata = get_company(orgnr)

        new_address = parse_address(dictdata)

        if registered_address != new_address:
            end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
            update_addresse((end_date, orgnr))
            insert_address([new_address])

        """
        GET THE COMPANY CODE OF THE CURRENT COMPANY AND CHECK IF ITS THE SAME
        """

        registered_orgform = select_orgform(orgnr)
        new_orgform = (
            dictdata['organisasjonsnummer'],
            dictdata['organisasjonsform']['kode'],
        )

        if registered_orgform == new_orgform:
            end_date = datetime.strftime(datetime.now(), format='%Y-%m-%d')
            update_orgform((end_date, orgnr))
            insert_orgform([new_orgform])
