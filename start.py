from os import path, system
from pathlib import Path
import json

import time

home = str(Path(Path.home()))
project_dir = path.join(home, 'powerlytics')
module_path = path.join('node_modules', 'node_red', 'red.js')

pm2_cmd = f'cd {project_dir} && pm2 start ecosystem.config.js  && ohmgraphite.exe start'

system(pm2_cmd)