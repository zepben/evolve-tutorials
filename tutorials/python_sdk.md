# How to use the Python SDK

The Evolve SDK provides the building blocks you need to interface with the rest of the platform. It can also be used to 
build your own solutions from scratch that will be compatible with other things built with the SDK.

## Getting Started
The Python SDK can be used by using the zepben.evolve package that can be installed in an environment by using pip
    
    pip install zepben.evolve

### Configuration Setup
These tutorials require a `config.json` file. This configuration file must follow this structure:

    {
      "auth0": {
        "client_id": "client_Id123",
        "username": "username123",
        "password": "password123",
        "conf_address": "config_address.com"
      },
      "ewb_server": {
        "host": "ewb_host",
        "port": 1234,
        "rpc_port": 1235,
        "secure": "True"
      },
      "eas_server": {
        "host": "eas_host",
        "port": 1236
      },
      "test_config": {
        "equipment_mrid": "equipment123",
        "feeder_mrid": "feeder123"
      }
    }
The `config.json` file is parsed and passed as a parameter called `config`

##Using the Python SDK
### Creating Objects
The Evolve platform is composed around a domain model based on the 'Common Information Model' (CIM). The CIM is a very 
large standard that covers a huge amount of use cases. To make things more digestible, Evolve publishes its own [CIM 
profile](https://zepben.github.io/evolve/docs/cim/evolve/). 

The following snippet of code showcases how to create Power
Transformers, Energy Consumers, Photovoltaic Units and Batteries:

    from zepben.evolve import PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit

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

### Connecting to a Server
It is also possible to interact, create or delete objects in a server. First, a connection with a set server must be established.
The following snippet showcases one way of establishing a connection with the [EWB Server](https://zepben.github.io/evolve/docs/energy-workbench-server/2.8.0).

    from zepben.evolve import connect, SyncNetworkConsumerClient 

    print("Connecting to Server...")
    with connect(host=config['ewb_server']['host'], rpc_port=config['ewb_server']['rpc_port'],
                 conf_address=config['auth0']['conf_address'],
                 client_id=config['auth0']['client_id'],
                 username=config['auth0']['username'],
                 password=config['auth0']['password'], secure=True) as channel:
        client = SyncNetworkConsumerClient(channel)
        print("Connection Established")

### Query Data From a Server
Extracting and querying data from a specific Feeder can be accomplished by using the mrid of the desired feeder. The 
next example displays the amount of Power Transformers, Energy Consumers, Photovoltaic Units and Batteries in the Feeder 
CPM3B3:

    from zepben.evolve import connect, SyncNetworkConsumerClient, NetworkService, \
        PowerTransformer, EnergyConsumer, PhotoVoltaicUnit, BatteryUnit
    
    with connect(host=config['ewb_server']['host'], rpc_port=config['ewb_server']['rpc_port'],
                 conf_address=config['auth0']['conf_address'],
                 client_id=config['auth0']['client_id'],
                 username=config['auth0']['username'],
                 password=config['auth0']['password'], secure=True) as channel:
        client = SyncNetworkConsumerClient(channel)
    
        feeder_mrid=config['test_config']['feeder_mrid']
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
Creating and uploading studies to the server using a script is possible. The following example showcases the creation of 
a very simple study. Once the study is created, it is automatically uploaded to the server and can be viewed in the 
_Study List_ in the EAS Web Client.

    from geojson import Feature, Point, LineString, FeatureCollection
    from zepben.eas import Study, EasClient
    
    from utils.style_creator import CircleStyle, LineStyle, InterpolateColor, LinePaint, CirclePaint
    
    print('Uploading study to EAS Server...')
        eas_client = EasClient(host=config['eas_server']['host'], port=config['eas_server']['port'],
                               client_id=config['auth0']['client_id'],
                               username=config['auth0']['username'],
                               password=config['auth0']['password'])
    
        feature1 = Feature(id='id1', geometry=Point((144.408936254, -37.6999353628)))
        feature2 = Feature(id='id2', geometry=Point((144.408936254, -37.99353628)))
        feature3 = Feature(id='id3', geometry=LineString([(144.408936254, -37.99353628), (144.408936254, -37.6999353628)]),
                           properties={"number": "100"})
        fc1 = FeatureCollection([feature1, feature2, feature3])
        fc2 = FeatureCollection([feature3])
    
        styles = [CircleStyle(style_id='circle').style,
                  LineStyle(style_id='line').style,
                  LineStyle(style_id='line_loading', paint=LinePaint(
                      line_color=InterpolateColor(to_number_name="number", limits=[0, 50, 100]).color()).paint).style,
                  CircleStyle(style_id='circle2', paint=CirclePaint(color="red").paint).style]
    
        result1 = Study.Result(name='2 x Circle &  1 x Line',
                               geo_json_overlay=Study.Result.GeoJsonOverlay(data=fc1, styles=['circle', 'line']))
        result2 = Study.Result(name='1 x Line',
                               geo_json_overlay=Study.Result.GeoJsonOverlay(data=fc2, styles=['line_loading']))
    
        results = [result1, result2]
    
        study = Study(
            name='Basic Study',
            description='',
            tags=['basic_study'],
            results=results,
            styles=styles
        )
    
        eas_client.upload_study(study)
    
        print(f'https://{config["eas_server"]["host"]}')