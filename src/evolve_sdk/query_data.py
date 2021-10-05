#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, \
    PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit


def query_data(feeder_mrid, evolve_client):
    print(f'Query data for Feeder: {feeder_mrid}')
    evolve_client.get_equipment_container(mrid=feeder_mrid)
    container: NetworkService = evolve_client.service

    power_transformers: [PowerTransformer] = list(container.objects(PowerTransformer))
    energy_consumers: [EnergyConsumer] = list(container.objects(EnergyConsumer))
    pv_units: [PhotoVoltaicUnit] = list(container.objects(PhotoVoltaicUnit))
    batteries: [BatteryUnit] = list(container.objects(BatteryUnit))

    print(f'Power Transformers in the feeder {feeder_mrid}: {len(power_transformers)}')
    print(f'Energy Consumers in the feeder {feeder_mrid}: {len(energy_consumers)}')
    print(f'Photovoltaic Units in the feeder {feeder_mrid}: {len(pv_units)}')
    print(f'Batteries in the feeder {feeder_mrid}: {len(batteries)}')
