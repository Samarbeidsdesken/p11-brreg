import psycopg2
from dbconnect.dbconfig import load_config

import pandas as pd

"""
New audits are inserted in the table database.tilsyn. The table is a copy of the data
provided by data.mattilsynet.no/smilefjes-tilsyn.csv. Same column headers. 

Old records are removed, and new recards are appendned. If there are any duplicates,
the database ignores them (ON CONFLICT DO NOTHING). 
"""

def insert_bostyrer(bostyrer, table = 'bostyrer'):

    """Insert a new konkurs into the table konkurser"""
    config = load_config()

    template = ','.join(['%s'] * len(bostyrer))
    sql = """
    INSERT INTO {} (orgnr, dato, type, bostyrer, gateadresse, poststed, epost, frist, fristdag) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                #cur.executemany(sql, tilsyn)
                cur.execute(sql, bostyrer)

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally: 
        print('The data records are inserted')
    
if __name__ == '__main__':
    pass