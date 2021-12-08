#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import *

from utils.utils import parse_auth_config

__all__ = ["connecting_ewb_server"]

def connecting_ewb_server(config):
    print("Connecting to Server...")

    # Connecting server
    with connect(host=config['ewb_server']['host'], rpc_port=config['ewb_server']['rpc_port'],
                 conf_address=config['auth0']['conf_address'],
                 client_id=config['auth0']['client_id'],
                 username=config['auth0']['username'],
                 password=config['auth0']['password'], secure=True) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connection Established")
    return client


if __name__ == '__main__':
    auth_config = parse_auth_config()
    connecting_ewb_server(auth_config)
