import psycopg2
from dbconnect.dbconfig import load_config

import pandas as pd


def insert_orgform(enheter, table='orgform'):
    """Insert a address into the table forretningsadresse"""
    config = load_config()

    template = ','.join(['%s'] * len(enheter))
    sql = """
    INSERT INTO {} (orgnr, orgform_kode) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, enheter)

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print('inserg orgform: '+ str(error))

    finally:
        pass


if __name__ == '__main__':
    pass
