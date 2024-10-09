import psycopg2
from dbconnect.dbconfig import load_config
from dbfunctions.dbinsert_enheter_oppdateringsid import insert_enheter_oppdateringsid

"""
Updates old records of roller when new roles are added.
"""


def update_enhet_slettet(orgnr, id = None):
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
        
        if id:
            insert_enheter_oppdateringsid(id, failed=False)

    except (Exception, psycopg2.DatabaseError) as error:
        print('update_enhet_slettet: ' + str(error))
        if id:
            insert_enheter_oppdateringsid(id, failed=True)
            
    finally:
        pass


if __name__ == '__main__':
    pass
