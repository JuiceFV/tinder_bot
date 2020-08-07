"""The file contains the function responsible for configuration loading.
"""
from pathlib import Path
import yaml

__all__ = ('upload_config',)


def upload_config(cfg_file=None):
    """The function which uploads a config from whether the default config-file nor passed config-file.

    :param cfg_file: passed config-file.
    :return: config-dict.
    """
    default_file = Path(__file__).parent.parent.parent / 'config.yaml'

    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cfg_dict = {}
    # if configuration file exists then upload the config as dict.
    if cfg_file:
        cfg_dict = yaml.safe_load(cfg_file)

    # if dict doesn't empty then update the config.
    if cfg_dict:
        config.update(**cfg_dict)

    return config
