# How to use the Python SDK

The Evolve SDK provides the building blocks you need to interface with the rest of the platform. It can also be used to 
build your own solutions from scratch that will be compatible with other things built with the SDK.

## Getting Started
The Python SDK can be used by using the zepben.evolve package that can be installed in an environment by using pip
    
    pip install zepben.evolve

### Creating Objects
The Evolve platform is composed around a domain model based on the 'Common Information Model' (CIM). The CIM is a very 
large standard that covers a huge amount of use cases. To make things more digestible, Evolve publishes its own [CIM 
profile](https://zepben.github.io/evolve/docs/cim/evolve/). 

The following snippet of code showcases how to create Power
Transformers, Energy Consumers, Photovoltaic Units and Batteries:

    from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit

    # Create a Power Transformer
    power_transformer = PowerTransformer(mrid="pt1")
    
    # Create EnergyConsumer
    energy_consumer = EnergyConsumer(mrid="ec1")
    
    # Create Photovoltaic Unit
    pv_unit = PhotoVoltaicUnit(mrid="pv1")
    
    # Create Battery
    battery = BatteryUnit(mrid="b1")

### Connecting to a Server
It is also possible to interact, create or delete objects in a server. First, a connection with set server must be established.
The following snippet showcases one way of establishing a connection with the [EWB Server](https://zepben.github.io/evolve/docs/energy-workbench-server/2.8.0).

    from zepben.evolve import connect, SyncNetworkConsumerClient 

    host = "evolve.essential.zepben.com"
    rpc_port = 443

    print("Connecting to Server")
    with connect(host=host, rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connection Established")

### Query Data From a Server
Extracting and querying data from a specific Feeder can be accomplished by using the mrid of the desired feeder. The 
next example displays the amount of Power Transformers, Energy Consumers, Photovoltaic Units and Batteries in the Feeder 
CPM3B3:

    from zepben.evolve import connect, SyncNetworkConsumerClient, NetworkService, \
        PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit

    host = "evolve.essential.zepben.com"
    rpc_port = 443
    
    print("Connecting to Server")
    with connect(host=host, rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connected to Server")
    
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

### Creating and Uploading Studies
Creating and uploading studies to the server using a Script is possible. 