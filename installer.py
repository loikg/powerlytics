from io import BytesIO 
from os import system, path, makedirs,  chdir
import os
import shutil
from urllib.request import urlopen
from zipfile import ZipFile
import json
import time
import sys
import logging

logger = logging.getLogger(__name__)

project_dir = 'C:\powerlytics'
npm_init = 'npm init -y'
node_red = 'npm install --save node-red'
flows_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/flows.json'
ohmgraphite_url = 'https://github.com/loikg/powerlytics/raw/main/OhmGraphite.exe'
ohmgraphite_config_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/OhmGraphite.exe.config'
ohmgraphire_nlog_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/NLog.config'
nssm_version = "2.24"
powerlytics_service_name = "powerlytics"
node_path = shutil.which(cmd="node")
nssm_path = path.join(project_dir, "nssm.exe")

flows_file_content = urlopen(flows_url)
ohmgraphite_content = urlopen(ohmgraphite_url)
ohmgraphite_config = urlopen(ohmgraphite_config_url).read()
ohmgraphite_nlog_content = urlopen(ohmgraphire_nlog_url).read()

API_URL = "{{API_URL}}"
API_URL = "{{PROD_API_URL}}",
APP_ID = "{{PROD_APP_ID}}",
TOKEN_URL = "{{PROD_TOKEN_URL}}",
AUTHORIZATION_URL = "{{PROD_AUTHORIZATION_URL}}"

def downloadNSSM(version: str):
  nssm_folder = f"nssm-{version}"
  nssm_exe_download_path = path.join(project_dir, nssm_folder, "win64", "nssm.exe")

  http_response = urlopen(f"https://nssm.cc/release/nssm-{version}.zip")
  zipfile = ZipFile(BytesIO(http_response.read()))
  zipfile.extractall()
  os.replace(src=nssm_exe_download_path, dst=path.join(project_dir, "nssm.exe"))
  shutil.rmtree(path=path.join(project_dir, nssm_folder))

def install_nodered_service():
  nodered_user_dir = path.join(project_dir, ".node-red")

  os.system(f'{nssm_path} install {powerlytics_service_name} "{node_path}"')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppDirectory {project_dir}')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppParameters "./node_modules/node-red/red.js --userDir {nodered_user_dir} -D contextStorage.default.module=memory -D contextStorage.file.module=localfilesystem"')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppEnvironmentExtra "NODE_TLS_REJECT_UNAUTHORIZED=0" "API_URL={API_URL}" "APP_ID={APP_ID}" "TOKEN_URL={TOKEN_URL}" "AUTHORIZATION_URL={AUTHORIZATION_URL}"')
  os.system(f'{nssm_path} set {powerlytics_service_name} Start SERVICE_AUTO_START')
  os.system(f'{nssm_path} set {powerlytics_service_name} Start SERVICE_AUTO_START')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppStdout {project_dir}\nodered-service.log')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppStderr {project_dir}\nodered-service.log')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppStdoutCreationDisposition 4')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppStderrCreationDisposition 4')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateFiles 1')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateOnline 0')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateSeconds 86400')
  os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateBytes 1048576')

if not path.exists(project_dir):
  os.makedirs(project_dir)

os.chdir(project_dir)

logging.basicConfig(level='INFO', filename=f'{project_dir}/logs.txt', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logging.info('Installing node-red')

system(f'{npm_init} && {node_red}')

logging.info('node-red installed')

with open(path.join(project_dir, 'flows.json'), 'w') as f:
  json.dump(json.loads(flows_file_content.read().decode('utf-8')), f)

with open(path.join(project_dir, 'OhmGraphite.exe'), 'wb') as f:
  f.write(ohmgraphite_content.read())

with open(path.join(project_dir, 'OhmGraphite.exe.config'), 'wb') as f:
  f.write(ohmgraphite_config)

with open(path.join(project_dir, 'NLog.config'), 'wb') as f:
  f.write(ohmgraphite_nlog_content)

ohmExe = path.join(project_dir, 'OhmGraphite.exe')

logging.info('Installing ohmgraphite')
ret = system(f'{ohmExe} install')
if not ret == 0:
  logging.exception(f'Installation failed with return code {ret}')
else:
  logging.info('Ohmgraphite installation successful!')

logging.info("Installing nssm.exe...")
try:
  downloadNSSM(version=nssm_version)
except Exception as err:
  logging.exception(f"Failed to download nssm.exe: {err}")
  sys.exit(1)
else:
  logging.info("Successfully installed nssm.exe")

logging.info("Installing nodered service...")
try:
  install_nodered_service()
except Exception as err:
    logging.exception(f"Failed to install nodered service: {err}")
    sys.exit(1)
else:
  logging.info("Successfully installed nodered service")

print('All services installed successfully!')

time.sleep(10)
