from configparser import ConfigParser
import os
import sys
from toolbox.userpath import get_path

def load_config(section='postgresql'):
    
    path = get_path()
    
    print(path)
    
    filename = path + 'secrets/database.ini'
    
    #with open('secrets/path_databaseini.txt') as f:
    #    filename = ''.join([line for line in f])
        
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)