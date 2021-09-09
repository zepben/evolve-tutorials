#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit


def creating_objects():

    print('Creating objects...')
    # Create a Power Transformer
    power_transformer = PowerTransformer(mrid="pt1")
    print(power_transformer)

    # Create EnergyConsumer
    energy_consumer = EnergyConsumer(mrid="ec1")
    print(energy_consumer)

    # Create Photovoltaic Unit
    pv_unit = PhotoVoltaicUnit(mrid="pv1")
    print(pv_unit)

    # Create Battery
    battery = BatteryUnit(mrid="b1")
    print(battery)
