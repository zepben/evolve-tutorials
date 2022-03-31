#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from utils.connect_to_server import connecting_ewb_server
from utils.utils import parse_auth_config

if __name__ == '__main__':
    auth_config = parse_auth_config()
    evolve_client = connecting_ewb_server(auth_config)

    print(f'Getting Network hierarchy...')
    result = evolve_client.get_network_hierarchy()
    print(f'Geographical regions:')
    for e in result.value.geographical_regions.values():
        print(e)
    print(f'Sub-geographical regions:')
    for e in result.value.geographical_regions.values():
        print(e)
    print(f'Feeders:')
    for e in result.value.feeders.values():
        print(e)