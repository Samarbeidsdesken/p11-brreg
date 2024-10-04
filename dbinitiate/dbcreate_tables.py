import psycopg2
from dbconnect.dbconfig import load_config


def create_table_bostyrer():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE bostyrer(
            id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
            orgnr CHARACTER VARYING(255) NULL,
            dato date NOT NULL,
            type CHARACTER VARYING(255) NOT NULL,
            bostyrer CHARACTER VARYING(255) NULL,
            gateadresse CHARACTER VARYING(255) NULL,
            poststed CHARACTER VARYING(255) NULL,
            epost CHARACTER VARYING(255) NULL,
            frist DATE NULL,
            fristdag DATE NULL
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


def create_table_konkurser():
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


def create_table_enheter():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE enheter (
            orgnr VARCHAR(255) PRIMARY KEY,
            navn VARCHAR(255),
            registreringsdatoenhetsregisteret DATE,
            stiftelsesdato DATE,            
            maalform VARCHAR(50),
            konkurs BOOLEAN,
            konkursdato DATE,
            is_active BOOLEAN DEFAULT TRUE, -- Boolean to track if a company is active or deleted
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def create_table_forretningsadresse():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE forretningsadresse (
            orgnr VARCHAR(255),
            forretningsadresse_adresse VARCHAR(255),
            forretningsadresse_postnummer CHAR(4),
            forretningsadresse_kommunenummer CHAR(4),
            forretningsadresse_land VARCHAR(255),
            forretningsadresse_landkode VARCHAR(10),
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list,
            CONSTRAINT pk_adresse_orgnr_enddate PRIMARY KEY (orgnr, end_date) -- Named composite primary key
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


def create_table_orgform():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE orgform (
            orgnr VARCHAR(255),
            orgform_kode VARCHAR(50),
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list,
            CONSTRAINT pk_orgform_orgnr_enddate PRIMARY KEY (orgnr, end_date) -- Named composite primary key
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


def create_table_roller():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE roller (
            orgnr character varying(255) NOT NULL,
            roller jsonb NOT NULL,
            id INTEGER NOT NULL DEFAULT 2858588, -- default is set to the change id value from which the tracking started
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list,
            CONSTRAINT pk_roller_orgnr_id PRIMARY KEY (orgnr, id) -- Named composite primary key
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


def create_table_company_contacts():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE company_contacts (
            orgnr character varying(255) NOT NULL,
            email character varying(255) NOT NULL,
            phone character varying(255) NOT NULL,
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list,
            CONSTRAINT pk_company_contact_orgnr_enddate PRIMARY KEY (orgnr, end_date) -- Named composite primary key
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


def create_table_company_nace():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE company_nace (
            orgnr character varying(255) NOT NULL,
            naeringskode1 character varying(255) NOT NULL,
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list
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

def create_table_employees():
    """ Create tables in the PostgreSQL database"""
    commands = (

        """
        CREATE TABLE employees (
            orgnr character varying(255) NOT NULL,
            employees INTEGER NOT NULL,
            is_current BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_date DATE -- End date is NULL if this is the current role list
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




if __name__ == '__main__':
    # create_tables()
    create_table_enheter()
