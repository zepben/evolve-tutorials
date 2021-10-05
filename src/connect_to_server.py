from zepben.evolve import *

host = "evolve.essential.zepben.com"
rpc_port = 443

print("Connecting to Server")
with connect(host=host, rpc_port=rpc_port,
             conf_address="https://evolve.essential.zepben.com/ewb/auth",
             client_id="8LCZNel8deS6Rcpt9Fv4ZgVMCzXI9uJ3",
             username="somerandomuser@bouckaert.com.au",
             password="Giraffe1354211", secure=True) as channel:
    client = SyncNetworkConsumerClient(channel)
    print("Connection Established")

    feeder_mrid = "CPM3B3"
    result = client.get_equipment_container(mrid=feeder_mrid)
    container: NetworkService = client.service

power_transformers: [PowerTransformer] = list(container.objects(PowerTransformer))
energy_consumers: [EnergyConsumer] = list(container.objects(EnergyConsumer))
pv_units: [PhotoVoltaicUnit] = list(container.objects(PhotoVoltaicUnit))
batteries: [BatteryUnit] = list(container.objects(BatteryUnit))

print(f'Power Transformers in the feeder {feeder_mrid}: {len(power_transformers)}')
print(f'Energy Consumers in the feeder {feeder_mrid}: {len(energy_consumers)}')
print(f'Photovoltaic Units in the feeder {feeder_mrid}: {len(pv_units)}')
print(f'Batteries in the feeder {feeder_mrid}: {len(batteries)}')

