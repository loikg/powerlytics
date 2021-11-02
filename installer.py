from os import system, path, makedirs
from urllib.request import urlopen

from pathlib import Path
import json

import time

import logging

logger = logging.getLogger(__name__)

home = str(Path(Path.home()))

data = '''
module.exports = {
  apps: [{
    name: "carbon-analytics",
    script: "./node_modules/node-red/red.js",
    env: {
      NODE_ENV: "development",
      NODE_TLS_REJECT_UNAUTHORIZED: 0,
      API_URL: "{{PROD_API_URL}}",
      APP_ID: "{{PROD_APP_ID}}",
      TOKEN_URL: "{{PROD_TOKEN_URL}}",
      AUTHORIZATION_URL: "{{PROD_AUTHORIZATION_URL}}"
    },
    env_test: {
      NODE_ENV: "test",
    },
    env_staging: {
      NODE_ENV: "staging",
    },
    env_production: {
      NODE_ENV: "production",
    }
  }]
}
'''

project_dir = path.join(home, 'powerlytics')
mkdir = f'mkdir {project_dir} && cd {project_dir}'

npm_init = 'npm init -y'

node_red = 'npm install --save node-red && npm install -g pm2'

flows_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/flows.json'

ohmgraphite_url = 'https://github.com/loikg/powerlytics/raw/main/OhmGraphite.exe'

ohmgraphite_config_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/OhmGraphite.exe.config'

ohmgraphire_nlog_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/NLog.config'

flows_file_content = urlopen(flows_url)

ohmgraphite_content = urlopen(ohmgraphite_url)

ohmgraphite_config = urlopen(ohmgraphite_config_url).read()

ohmgraphite_nlog_content = urlopen(ohmgraphire_nlog_url).read()

if not path.exists(project_dir):
  makedirs(project_dir)
 
logging.basicConfig(level='INFO', filename=f'{project_dir}/logs.txt', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logging.info('Installing node-red')

system(f'cd {project_dir} && {npm_init} && {node_red}')

logging.info('node-red installed')

with open(path.join(project_dir, 'ecosystem.config.js'), 'w') as f:
    f.write(data)    

with open(path.join(project_dir, 'flows.json'), 'w') as f:
    json.dump(json.loads(flows_file_content.read().decode('utf-8')), f)

with open(path.join(project_dir, 'ohmgraphite.exe'), 'wb') as f:
  f.write(ohmgraphite_content.read())

with open(path.join(project_dir, 'ohmgraphite.exe.config'), 'wb') as f:
  f.write(ohmgraphite_config)

with open(path.join(project_dir, 'NLog.config'), 'wb') as f:
  f.write(ohmgraphite_nlog_content)

with open(path.join(project_dir, '.count'), 'w') as f:
  pass

ohmExe = path.join(project_dir, 'ohmgraphite.exe')

logging.info('Installing ohmgraphite')
system(f'{ohmExe} install')
logging.info('Ohmgraphite installation successful!')

print('All services started successfully!')

# print("you can now visit http://localhost:1880 to browse the node-red ui")

time.sleep(10)
