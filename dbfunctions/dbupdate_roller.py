import psycopg2
from dbconnect.dbconfig import load_config

import pandas as pd

"""
Updates old records of roller when new roles are added.
"""


def insert_roller_update(data):
    """Insert a new rolle into the table roller"""
    config = load_config()

    # Define the SQL update query
    sql = """
        UPDATE roller
        SET is_current = false, 
            end_date = %s
        WHERE orgnr = %s AND is_current = true;
        """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, data)

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        print('The data records are inserted')


if __name__ == '__main__':
    pass
