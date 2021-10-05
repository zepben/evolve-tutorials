from zepben.evolve import *

host = "evolve.essential.zepben.com"
rpc_port = 443


def connecting_server(config):
    print("Connecting to Server...")

    with open(config['ewb_server']['ca_path'], "rb") as f:
        ca = f.read()

    with connect(host=host, rpc_port=rpc_port,
                 conf_address="https://evolve.essential.zepben.com/ewb/auth",
                 client_id="8LCZNel8deS6Rcpt9Fv4ZgVMCzXI9uJ3",
                 username="somerandomuser@bouckaert.com.au",
                 password="Giraffe1354211", secure=True, ca=ca) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connection Established")
