import json
from dataclasses import dataclass

import pytest


@dataclass
class Auth0:
    client_id: str
    username: str
    password: str
    conf_address: str


@dataclass
class EwbServerConfig:
    host: str

    port: int = 9000
    rpc_port: int = 443
    secure: bool = False


@dataclass
class EasServerConfig:
    host: str
    port: int = 7654


@dataclass
class TestConfig:
    equipment_mrid: str
    feeder_mrid: str


class Config:
    def __init__(self, config_json: {}):
        self.auth0 = Auth0(username=config_json['auth0']['username'],
                           password=config_json['auth0']['password'], client_id=config_json['auth0']['client_id'],
                           conf_address=config_json['auth0']['conf_address'])
        secure = False
        if config_json['ewb_server']['secure'] == "True":
            secure = True

        self.ewb_server = EwbServerConfig(host=config_json['ewb_server']['host'],
                                          port=config_json['ewb_server']['port'],
                                          rpc_port=config_json['ewb_server']['rpc_port'],
                                          secure=secure)
        self.eas_server = EasServerConfig(host=config_json['eas_server']['host'],
                                          port=config_json['eas_server']['port'])
        self.test_config = TestConfig(equipment_mrid=config_json['test_config']['equipment_mrid'],
                                      feeder_mrid=config_json['test_config']['feeder_mrid'])


@pytest.fixture
def config():
    with open('../config_file/config.json') as config_file:
        data = json.load(config_file)
    return Config(data)
