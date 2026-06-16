import importlib
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def load_config():
    with open(os.path.join(PROJECT_ROOT, 'adapter_config.json'), encoding='utf-8') as f:
        return json.load(f)


def log_project_config():
    path = os.path.join(PROJECT_ROOT, 'project_config.json')
    with open(path, encoding='utf-8') as f:
        proj = json.load(f)
    gs = proj.get('google_sheets', {})
    logger.info("=" * 80)
    logger.info("PROJECT CONFIGURATION")
    logger.info("=" * 80)
    logger.info(f"  Environment     : {gs.get('environment', 'N/A')}")
    logger.info(f"  Sheet Name      : {gs.get('sheet_name', 'N/A')}")
    logger.info(f"  Target Folder ID: {gs.get('target_folder_id', 'N/A')}")
    logger.info("=" * 80)


def run_adapter(adapter_cfg):
    adapter_id = adapter_cfg['adapter_id']
    portal = adapter_cfg['portal']
    logger.info(f"{'=' * 80}")
    logger.info(f"Adapter: {adapter_id} | Portal: {portal} | Type: {adapter_cfg['type']} | Freq: {adapter_cfg['frequency']}")
    logger.info(f"{'=' * 80}")
    module = importlib.import_module(adapter_cfg['module'])
    module.main()


def main(adapter_filter=None):
    log_project_config()
    config = load_config()
    adapters = config.get('adapters', [])

    if not adapters:
        logger.warning("No adapters configured in adapter_config.json")
        return

    for adapter in adapters:
        if not adapter.get('enabled', True):
            logger.info(f"Skipping disabled adapter: {adapter['adapter_id']}")
            continue
        if adapter_filter and adapter['adapter_id'] != adapter_filter:
            continue
        run_adapter(adapter)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    # Optional: pass adapter_id as argument to run a single adapter
    # e.g. python orchestrator.py adapter1
    adapter_filter = sys.argv[1] if len(sys.argv) > 1 else None
    main(adapter_filter)
