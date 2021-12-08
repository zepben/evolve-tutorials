#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio

from eas.upload_studies import upload_study
from evolve_sdk.connect_to_server import connecting_ewb_server
from evolve_sdk.creating_objects import creating_objects
from evolve_sdk.hosting_capacity import hosting_capacity
from evolve_sdk.load_flow import load_flow
from evolve_sdk.query_data import query_data
from utils.config_reader import read_config

if __name__ == '__main__':
    # Reading config file
    auth_config = read_config()[0]

    # evolve-sdk-python examples
    creating_objects()
    client = connecting_ewb_server(auth_config)
    query_data(evolve_client=client, feeder_mrid=auth_config['test_config']['feeder_mrid'])

    # eas examples
    upload_study(auth_config)

    # load flow
    asyncio.run(load_flow())

    # hosting capacity
    asyncio.run(hosting_capacity())
