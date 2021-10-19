from os import system, path
from urllib.request import urlopen

from pathlib import Path
import json

import time

home = str(Path(Path.home()))

data = '''
module.exports = {
  apps: [{
    name: "carbon-analytics",
    script: "./node_modules/node-red/red.js",
    env: {
      NODE_ENV: "development",
      NODE_TLS_REJECT_UNAUTHORIZED: 0,
      API_URL: "https://f25a7443-be65-4cd1-a3ea-2b6431a9e63c.cloudapp.net/metrics",
      APP_ID: "cf2396bd-0875-40df-8244-15d2fa92a940",
      TOKEN_URL: "https://login.microsoftonline.com/9dae36f4-0de6-4a4e-a718-3dc11e509f38/oauth2/v2.0/token",
      AUTHORIZATION_URL: "https://login.microsoftonline.com/9dae36f4-0de6-4a4e-a718-3dc11e509f38/oauth2/v2.0/authorize"
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

system(f'{mkdir} && {npm_init} && {node_red}')

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

system('ohmgraphite.exe install')

print('All services started successfully!')

print("you can now visit http://localhost:1880 to browse the node-red ui")

time.sleep(10)