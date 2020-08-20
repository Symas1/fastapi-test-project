import os

from config.utils import load_conf

ENVIRONMENT_TYPE = os.environ['ENVIRONMENT_TYPE']
CONF = load_conf(filepath=f'config/{ENVIRONMENT_TYPE}.yml')
