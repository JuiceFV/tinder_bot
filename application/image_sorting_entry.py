import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from application.sources.config_handler import upload_config
from application.sources.image_clusterization import classify_images_to_like_dislike, classify_images_per_user
import argparse

parser = argparse.ArgumentParser(description="Tinder-Bot image clusterization")
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help="Path to configuration file")
parser.add_argument('-m', '--mode', help="Type of classifying of images", default='overall')
args = parser.parse_args()

if args.mode == 'user':
    classify_images_per_user(names=upload_config(args.config)['canvas']['judges']['names'])
elif args.mode == 'overall':
    classify_images_to_like_dislike(names=upload_config(args.config)['canvas']['judges']['names'])
else:
    print("You've typed wrong type of classifier. It is possible the only user or overall.")

