import yaml
import os.path as op
from pathlib import Path


# will try to find the first folder
CONFIG_FILE_PATHS = [
    op.join(op.dirname(__file__), '..', 'config'),
    op.join(op.expanduser('~'), '.config', 'lunchbot'),
    '/etc/lunchbot',
    # one more added at runtime!
]

def _find_git_root():
    this_file_dir = Path(op.abspath(op.dirname( __file__ )))
    for folder in reversed(this_file_dir.parents):
        if op.isdir(op.join(folder, '.git')):
            return folder


def _get_cfg_dir():
    # add path relative to GIT root, useful when running from GIT clone
    git_root = _find_git_root()
    if git_root is None:
        config_file_paths = CONFIG_FILE_PATHS
    else:
        config_file_paths = (CONFIG_FILE_PATHS +
                             [op.join(git_root, 'config')])

    for cfg_path in config_file_paths:
        if op.isdir(cfg_path):
            return cfg_path
    else:
        raise RuntimeError(f"No config file path not found "
                           "(search paths: {config_file_paths})")


def slack_bot_token():
    fname = op.join(_get_cfg_dir(), 'secrets.yml')
    with open(fname, 'r') as f:
        secrets = yaml.load(f.read())
    return secrets['slack_bot_token']
