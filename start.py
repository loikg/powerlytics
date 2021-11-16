from os import path, system
import os
import logging
import subprocess
import shutil

logging.getLogger(__name__)


project_dir = 'C:\powerlytics'
ohm_path = path.join(project_dir, "OhmGraphite.exe")
nssm_path = path.join(project_dir, "nssm.exe")
powerlytics_service = "powerlytics"
node_path = shutil.which(cmd="node")

logging.basicConfig(level='INFO', filename=f'{project_dir}/logs.txt', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
os.chdir(project_dir)


nodered_env = {
    'NODE_TLS_REJECT_UNAUTHORIZED': '0',
    'API_URL': 'https://f25a7443-be65-4cd1-a3ea-2b6431a9e63c.cloudapp.net/metrics',
    'APP_ID' : 'cf2396bd-0875-40df-8244-15d2fa92a940',
    'TOKEN_URL': 'https://login.microsoftonline.com/9dae36f4-0de6-4a4e-a718-3dc11e509f38/oauth2/v2.0/token',
    'AUTHORIZATION_URL': 'https://login.microsoftonline.com/9dae36f4-0de6-4a4e-a718-3dc11e509f38/oauth2/v2.0/authorize'
}

process_env = {**os.environ, **nodered_env}

nodered_userDir = path.join(project_dir, '.node-red')

# Run nodered with node in the background
subprocess.run([
    node_path, 
    './node_modules/node-red/red.js', 
    '--userDir', nodered_userDir, 
    '-D', 'contextStorage.default.module=memory', 
    '-D', 'contextStorage.file.module=localfilesystem'], 
    env=process_env,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=8,
    cwd=project_dir)