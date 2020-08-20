import os

from config.utils import load_conf

ENVIRONMENT_TYPE = os.environ.get('ENVIRONMENT_TYPE', 'base')
CONF = load_conf(filepath=f'config/{ENVIRONMENT_TYPE}.yml')
