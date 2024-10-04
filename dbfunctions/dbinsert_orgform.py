import psycopg2
from dbconnect.dbconfig import load_config
from dbfunctions.dbinsert_enheter_oppdateringsid import insert_enheter_oppdateringsid


def insert_orgform(enheter, id, table='orgform'):
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
                
        
        insert_enheter_oppdateringsid(id, False)
            

    except (Exception, psycopg2.DatabaseError) as error:
        insert_enheter_oppdateringsid(id, failed=True)
        print('inserg orgform: '+ str(error))

    finally:
        pass


if __name__ == '__main__':
    pass
