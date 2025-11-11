"""
Configuration loader for mini-judge.

Reads required Redis settings from mini-judge.conf.
Raises ValueError if any required setting is missing.

Attributes:
    mini_judge_config (dict): Dictionary containing 'host', 'port', and 'db' for Redis connection.
"""

import configparser

config = configparser.ConfigParser()
config.read("mini-judge.conf")

required_keys = ['REDIS_HOST', 'REDIS_PORT','QUEUE_NAME']
section = 'REDIS'

if not config.has_section(section):
    raise ValueError(f"Missing section [{section}] in config file.")

mini_judge_config = {}
for key in required_keys:
    if not config.has_option(section, key):
        raise ValueError(f"Missing required config: [{section}] {key}")
    mini_judge_config[key] = config.get(section, key)

# Convert port and db to int
mini_judge_config['REDIS_HOST'] = mini_judge_config['REDIS_HOST']
mini_judge_config['REDIS_PORT'] = int(mini_judge_config['REDIS_PORT'])
mini_judge_config['QUEUE_NAME'] = mini_judge_config['QUEUE_NAME']