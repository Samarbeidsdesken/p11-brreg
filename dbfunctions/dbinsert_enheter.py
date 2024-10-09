import psycopg2
from dbconnect.dbconfig import load_config
from dbfunctions.dbinsert_enheter_oppdateringsid import insert_enheter_oppdateringsid

"""
New audits are inserted in the table database.tilsyn. The table is a copy of the data
provided by data.mattilsynet.no/smilefjes-tilsyn.csv. Same column headers. 

Old records are removed, and new recards are appendned. If there are any duplicates,
the database ignores them (ON CONFLICT DO NOTHING). 
"""


def insert_company(enheter, table='enheter', id = None):
    """Insert a new rolle into the table roller"""
    config = load_config()

    template = ','.join(['%s'] * len(enheter))
    sql = """
    INSERT INTO {} (orgnr, navn, registreringsdatoenhetsregisteret, stiftelsesdato, maalform, konkurs, konkursdato) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, enheter)

                conn.commit()
        
        if id:
            insert_enheter_oppdateringsid(id, failed=False)

    except (Exception, psycopg2.DatabaseError) as error:
        if id:
            insert_enheter_oppdateringsid(id, failed=True)
        print(error)

    finally:
        pass


if __name__ == '__main__':
    pass
