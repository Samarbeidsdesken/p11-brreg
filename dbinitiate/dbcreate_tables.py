import psycopg2
from dbconnect.dbconfig import load_config

def create_table_bostyrer():
    """ Create tables in the PostgreSQL database"""
    commands = (
        
        """
        CREATE TABLE bostyrer(
            id INT GENERATED ALWAYS AS IDENTITY,
            orgnr VARCHAR(255),
            dato date NOT NULL,
            type character varying(255) NOT NULL,
            bostyrer VARCHAR(255),
            gateadresse VARCHAR(255),
            poststed VARCHAR(255),
            epost VARCHAR(255),
            frist DATE,
            fristdag DATE,
            FOREIGN KEY(orgnr, dato, type) REFERENCES konkurser(orgnr, dato, type)
            
        );
        """
        ),
        

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        
        """
        CREATE TABLE konkurser(
            navn VARCHAR(255),
            orgnr VARCHAR(255),
            dato DATE,
            type VARCHAR(255),
            url VARCHAR(255),
            PRIMARY KEY(orgnr, dato)
        )
        """
        ),
        

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    #create_tables()
    create_table_bostyrer()