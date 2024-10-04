import psycopg2
from dbconnect.dbconfig import load_config

"""
Updates old records of roller when new roles are added.
"""


def update_enhet_konkurs(data):
    """Update a company if it is bankrupt"""
    config = load_config()

    # Define the SQL update query
    sql = """
        UPDATE enheter
        SET konkurs = true,
        SET konkursdato = {}
        WHERE orgnr = '{}';
        """.format(
            data[0],
            data[1]
            )

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
