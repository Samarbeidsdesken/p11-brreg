import psycopg2
from dbconnect.dbconfig import load_config


def select_enheter_maxid(table='enheter_oppdateringsid'):
    """Get last oppdateringsid"""
    config = load_config()

    sql = """
    SELECT MAX(id) FROM {table};
    """.format(
        table=table
        )

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # cur.executemany(sql, tilsyn)
                cur.execute(sql)

                # return all results from the query
                return str(cur.fetchone()[0])

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
