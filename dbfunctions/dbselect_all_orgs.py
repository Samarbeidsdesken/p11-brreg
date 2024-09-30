import psycopg2
from dbconnect.dbconfig import load_config

import pandas as pd


def select_orgs(table='enheter'):
    """Get all companies in database"""
    config = load_config()

    sql = """
    SELECT orgnr from {table};
    """.format(table=table)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql)

                # Fetch all results from the query
                result = cur.fetchall()

                # Return the result as a list
                return [row[0] for row in result]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        # Ensure the cursor and connection are closed properly
        if cur:
            cur.close()
        if conn:
            conn.close()

    return None


if __name__ == '__main__':
    pass
