import psycopg2
from dbconnect.dbconfig import load_config

"""
New audits are inserted in the table database.tilsyn. The table is a copy of the data
provided by data.mattilsynet.no/smilefjes-tilsyn.csv. Same column headers. 

Old records are removed, and new recards are appendned. If there are any duplicates,
the database ignores them (ON CONFLICT DO NOTHING). 
"""


def insert_roller(roller, table='roller', remote = False):
    """Insert a new rolle into the table roller"""
    config = load_config(remote = remote)

    template = ','.join(['%s'] * len(roller))
    sql = """
    INSERT INTO {} (orgnr, id, roller) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, roller)

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        pass


if __name__ == '__main__':
    pass
