import os
import json

# All shared configuration lives in the root config.py.
# This shim re-exports everything from there and overrides only the
# paths and identifiers that are specific to this adapter.
from config import *   # noqa: F401, F403

# Adapter-specific path overrides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'adapter1.log')

# Read adapter_id from root config.json so it stays in sync with one source of truth
_config_json_path = os.path.join(BASE_DIR, '..', '..', 'config.json')
with open(_config_json_path) as _f:
    _adapters = json.load(_f).get('adapters', [])

# Derive this adapter's folder name from BASE_DIR and match case-insensitively
# so capitalisation differences in config.json never cause a miss.
_this_adapter = os.path.basename(BASE_DIR).lower()
ADAPTER_ID = next(
    (a['adapter_id'] for a in _adapters if a.get('adapter_id', '').lower() == _this_adapter),
    'NA'
)
