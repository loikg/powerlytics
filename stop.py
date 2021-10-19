from os import path, system
from pathlib import Path
import json

import time

home = str(Path(Path.home()))
project_dir = path.join(home, 'powerlytics')

pm2_cmd = f'cd {project_dir} && pm2 kill  && ohmgraphite.exe stop'

system(pm2_cmd)