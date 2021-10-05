from evolve_sdk.connect_to_server import connecting_server
from evolve_sdk.creating_objects import creating_objects
from evolve_sdk.query_data import query_data
from utils.config_reader import read_config

if __name__ == '__main__':
    config = read_config()[0]
    creating_objects()
    client = connecting_server(config)
    query_data(evolve_client=client, feeder_mrid=config['test_config']['feeder_mrid'])

