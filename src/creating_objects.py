from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit

# Create a Power Transformer
power_transformer = PowerTransformer(mrid="pt1")

# Create EnergyConsumer
energy_consumer = EnergyConsumer(mrid="ec1")

# Create Photovoltaic Unit
pv_unit = PhotoVoltaicUnit(mrid="pv1")

# Create Battery
battery = BatteryUnit(mrid="b1")