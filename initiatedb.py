
# from dbinitiate.dbcreate_tables import create_table_bostyrer
# from dbinitiate.dbcreate_tables import create_table_konkurser

from dbinitiate.dbcreate_tables import create_table_enheter
from dbinitiate.dbcreate_tables import create_table_forretningsadresse
from dbinitiate.dbcreate_tables import create_table_orgform
from dbinitiate.dbcreate_tables import create_table_roller


if __name__ == '__main__':
    # create_table_konkurser();
    # create_table_bostyrer()

    create_table_enheter()
    create_table_roller()
    create_table_orgform()
    create_table_forretningsadresse()
