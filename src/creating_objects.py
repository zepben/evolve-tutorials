from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit


def creating_objects():

    print('Printing created objects...')
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
