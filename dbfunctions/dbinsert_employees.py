import psycopg2
from dbconnect.dbconfig import load_config
from dbfunctions.dbinsert_enheter_oppdateringsid import insert_enheter_oppdateringsid


def insert_employees(enheter, id = None, table='employees', remote = False):
    """Insert a address into the table forretningsadresse"""
    config = load_config(remote = remote)

    template = ','.join(['%s'] * len(enheter))
    sql = """
    INSERT INTO {} (orgnr, employees) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, enheter)

                conn.commit()
        
        if id:
            insert_enheter_oppdateringsid(id, failed = False)
        

    except (Exception, psycopg2.DatabaseError) as error:
        print('inserg orgform: '+ str(error))
        if id:
            insert_enheter_oppdateringsid(id, failed = True)

    finally:
        pass


if __name__ == '__main__':
    pass
