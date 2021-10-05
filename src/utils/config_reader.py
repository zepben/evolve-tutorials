import argparse
import json


def read_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()
    with open(args.config) as f:
        cf = json.load(f)
    return [cf, args]
