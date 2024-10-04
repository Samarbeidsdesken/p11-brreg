import psycopg2
from dbconnect.dbconfig import load_config
from dbfunctions.dbinsert_enheter_oppdateringsid import insert_enheter_oppdateringsid



def insert_address(enheter, id, table='forretningsadresse'):
    """Insert a address into the table forretningsadresse"""
    config = load_config()

    template = ','.join(['%s'] * len(enheter))
    sql = """
    INSERT INTO {} (orgnr, forretningsadresse_adresse, forretningsadresse_postnummer, forretningsadresse_kommunenummer, forretningsadresse_land, forretningsadresse_landkode) values {} ON CONFLICT DO NOTHING;
    """.format(table, template)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql, enheter)

                conn.commit()
                
        insert_enheter_oppdateringsid(id, failed=False)

    except (Exception, psycopg2.DatabaseError) as error:
        print('insert_address: ' + str(error))
        insert_enheter_oppdateringsid(id, failed=True)

    finally:
        pass


if __name__ == '__main__':
    pass
