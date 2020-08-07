import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from application.sources import Validator
from application.sources.config_handler import upload_config
import argparse

parser = argparse.ArgumentParser(description="Tinder-Bot user's validator")
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Path to configuration file")
args = parser.parse_args()

validator = Validator(config=upload_config(args.config))
validator.start()
