import argparse
import json
import logging
from logging import Logger
from typing import Dict

from zepben.evolve import NetworkConsumerClient

__all__ = ["get_logger", "read_json_config", "get_random_color", "get_feeder_network", "parse_auth_config"]


async def get_feeder_network(channel, feeder_mrid):
    client = NetworkConsumerClient(channel)
    (await client.get_equipment_container(mrid=feeder_mrid)).throw_on_error()
    return client.service


def get_random_color():
    count = 0
    colors = [
        "#696969",
        "#2e8b57",
        "#7f0000",
        "#808000",
        "#000080",
        "#ff0000",
        "#ff8c00",
        "#ffd700",
        "#ba55d3",
        "#00ff7f",
        "#0000ff",
        "#f08080",
        "#adff2f",
        "#ff00ff",
        "#1e90ff",
        "#dda0dd",
        "#87ceeb",
        "#ff1493",
        "#7fffd4",
        "#ffe4c4"
    ]

    while True:
        count = (count + 1) % len(colors)
        yield colors[count]


def get_logger() -> Logger:
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


def read_json_config(config_file_path: str) -> Dict:
    file = open(config_file_path)
    config_dict = json.load(file)
    file.close()
    return config_dict


def parse_auth_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()
    with open(args.config) as f:
        cf = json.load(f)
    return cf
