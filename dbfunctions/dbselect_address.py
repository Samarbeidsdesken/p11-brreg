import psycopg2
from dbconnect.dbconfig import load_config


def select_address(orgnr, table='forretningsadresse'):
    """Get all companies in database"""
    config = load_config()

    sql = """
    SELECT orgnr, forretningsadresse_adresse, forretningsadresse_postnummer, forretningsadresse_kommunenummer, forretningsadresse_land, forretningsadresse_landkode from {table} WHERE orgnr = '{orgnr}' AND is_current = true;
    """.format(
        table=table,
        orgnr=orgnr
    )

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql)
                
                 # return all results from the query
                result = cur.fetchall()
                if len(result) == 0:
                    return None
                elif len(result) == 1:
                    return result[0]
                else:
                    return result

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
