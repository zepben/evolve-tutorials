from connect_to_server import connecting_server
from creating_objects import creating_objects
from utils.config_reader import read_config

if __name__ == '__main__':
    config = read_config()[0]
    connecting_server(config)
    creating_objects()