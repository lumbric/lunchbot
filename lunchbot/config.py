import yaml
import os.path as op


# will try to find the first folder
CONFIG_FILE_PATHS = [
    op.join(op.dirname(__file__), '..', 'config'),
    op.join(op.expanduser('~'), '.config', 'lunchbot'),
    '/etc/lunchbot',
]


def _get_cfg_dir():
    for cfg_path in CONFIG_FILE_PATHS:
        if op.isdir(cfg_path):
            return cfg_path
    else:
        raise RuntimeError("No config file path not found "
                           "(search paths: {CONFIG_FILE_PATHS})")


def slack_api_token():
    fname = op.join(_get_cfg_dir(), 'secrets.yml')
    with open(fname, 'r') as f:
        secrets = yaml.load(f.read())
    return secrets['slack_api_token']
