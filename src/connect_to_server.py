from zepben.evolve import *

host = "evolve.essential.zepben.com"
rpc_port = 443


def connecting_server(config):
    print("Connecting to Server...")

    # Reading certificate
    with open(config['ewb_server']['ca_path'], "rb") as f:
        ca = f.read()

    # Connecting server
    with connect(host=config['ewb_server']['host'], rpc_port=config['ewb_server']['rpc_port'],
                 conf_address=config['auth0']['conf_address'],
                 client_id=config['auth0']['client_id'],
                 username=config['auth0']['username'],
                 password=config['auth0']['password'], secure=True, ca=ca) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connection Established")
