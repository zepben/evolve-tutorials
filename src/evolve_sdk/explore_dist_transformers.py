#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from utils.connect_to_server import connecting_ewb_server, NetworkService, PowerTransformer
from utils.utils import parse_auth_config

if __name__ == '__main__':
    auth_config = parse_auth_config()
    evolve_client = connecting_ewb_server(auth_config)
    print(f'Getting Feeder IDs:')
    result = evolve_client.get_network_hierarchy()
    for e in result.value.feeders.values():
        print(f'Explore Distribution Transformers for the feeder: {e.mrid}')
        evolve_client.get_equipment_container(e.mrid).throw_on_error()
        container: NetworkService = evolve_client.service
        power_transformers: [PowerTransformer] = list(container.objects(PowerTransformer))
        print(f'Printing r and x for all the distribution transformers for the feeder: {e.mrid}')
        for tx in power_transformers:
            print(f'Power Transformer mRID: {tx.mrid}')
            for end in tx.ends:
                print(f'PTEnd: {end.mrid}')
                print(f'r: {end.star_impedance.r}')
                print(f'x: {end.star_impedance.x}')