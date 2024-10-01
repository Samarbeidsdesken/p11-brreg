import psycopg2
from dbconnect.dbconfig import load_config

import pandas as pd

"""
Updates old records of roller when new roles are added.
"""


def update_enhet_slettet(orgnr):
    """Insert a new rolle into the table roller"""
    config = load_config()

    # Define the SQL update query
    sql = """
        UPDATE enheter
        SET is_active = false
        WHERE orgnr = '{}';
        """.format(orgnr)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql)

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print('update_enhet_slettet: ' + str(error))

    finally:
        pass


if __name__ == '__main__':
    pass
