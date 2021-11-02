from os import path, system
from pathlib import Path
import json

import time

import logging

logging.getLogger(__name__)

home = str(Path(Path.home()))
project_dir = path.join(home, 'powerlytics')
module_path = path.join('node_modules', 'node_red', 'red.js')

pm2_cmd = f'cd {project_dir} && pm2 start ecosystem.config.js  && .\ohmgraphite.exe start'

ret = system(pm2_cmd)

if not ret==0:
    logging.exception(f'Failed to start all services with code {ret}')
logging.info('All services started, please go to http://localhost:1880')