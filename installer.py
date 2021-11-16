from os import getcwd, system, path, makedirs,  chdir
import os
import shutil
from urllib.request import urlopen
import json
import time
import logging
import win32com.client

logger = logging.getLogger(__name__)

project_dir = 'C:\powerlytics'
npm_init = 'npm init -y'
node_red = 'npm install --save node-red'
flows_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/flows.json'
ohmgraphite_url = 'https://github.com/loikg/powerlytics/raw/main/OhmGraphite.exe'
ohmgraphite_config_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/OhmGraphite.exe.config'
ohmgraphire_nlog_url = 'https://raw.githubusercontent.com/loikg/powerlytics/main/NLog.config'
# nssm_version = "2.24"
# powerlytics_service_name = "powerlytics"
node_path = shutil.which(cmd="node")
# nssm_path = path.join(project_dir, "nssm.exe")
start_exe_path = path.join(project_dir, "start.exe")

flows_file_content = urlopen(flows_url)
ohmgraphite_content = urlopen(ohmgraphite_url)
ohmgraphite_config = urlopen(ohmgraphite_config_url).read()
ohmgraphite_nlog_content = urlopen(ohmgraphire_nlog_url).read()

# API_URL = "",
# APP_ID = "abc",
# TOKEN_URL = "http://token",
# AUTHORIZATION_URL = "http://auth"

TASK_TRIGGER_LOGON = 9
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
TASK_RUNLEVEL_HIGHEST = 1

# Create and register a task with windows task scheduler to start nodered on user logon.
def register_nodered_window_task():
  task_name = 'Powerlytics'
  scheduler = win32com.client.Dispatch('Schedule.Service')
  scheduler.Connect()
  root_folder = scheduler.GetFolder('\\')

  # Create a user loggon triggerred tasks
  task_def = scheduler.NewTask(0)
  task_def.Triggers.Create(TASK_TRIGGER_LOGON)

  # Add command excution action to trigger
  action = task_def.Actions.Create(TASK_ACTION_EXEC)
  action.Path = start_exe_path
  action.WorkingDirectory = project_dir

  # Set task common parameters
  task_def.RegistrationInfo.Description = 'Start powerlytics'
  task_def.Settings.Enabled = True
  task_def.Settings.StopIfGoingOnBatteries = False
  task_def.Settings.DisallowStartIfOnBatteries = False # start the task regradless of the laptop being on battery or not

  # Run task as admin
  task_def.Principal.RunLevel = TASK_RUNLEVEL_HIGHEST

  root_folder.RegisterTaskDefinition(
    task_name,
    task_def,
    TASK_CREATE_OR_UPDATE,
    '',  # No user
    '',  # No password
    TASK_LOGON_NONE)

  # Manually Run task
  task = root_folder.GetTask(f'\{task_name}')
  task.Run(None)

# def downloadNSSM(version: str):
#   nssm_folder = f"nssm-{version}"
#   nssm_exe_download_path = path.join(project_dir, nssm_folder, "win64", "nssm.exe")

#   http_response = urlopen(f"https://nssm.cc/release/nssm-{version}.zip")
#   zipfile = ZipFile(BytesIO(http_response.read()))
#   zipfile.extractall()
#   os.replace(src=nssm_exe_download_path, dst=path.join(project_dir, "nssm.exe"))
#   shutil.rmtree(path=path.join(project_dir, nssm_folder))

# def install_nodered_service():
#   nodered_user_dir = path.join(project_dir, ".node-red")
#   nodered_svc_log_path = path.join(project_dir, "nodered-service.log")

#   os.system(f'{nssm_path} install {powerlytics_service_name} "{node_path}"')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppDirectory {project_dir}')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppParameters "./node_modules/node-red/red.js --userDir {nodered_user_dir} -D contextStorage.default.module=memory -D contextStorage.file.module=localfilesystem"')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppEnvironmentExtra "NODE_TLS_REJECT_UNAUTHORIZED=0" "API_URL={API_URL}" "APP_ID={APP_ID}" "TOKEN_URL={TOKEN_URL}" "AUTHORIZATION_URL={AUTHORIZATION_URL}"')
#   os.system(f'{nssm_path} set {powerlytics_service_name} Start SERVICE_AUTO_START')
#   os.system(f'{nssm_path} set {powerlytics_service_name} Start SERVICE_AUTO_START')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppStdout {nodered_svc_log_path}')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppStderr {nodered_svc_log_path}')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppStdoutCreationDisposition 4')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppStderrCreationDisposition 4')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateFiles 1')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateOnline 0')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateSeconds 86400')
#   os.system(f'{nssm_path} set {powerlytics_service_name} AppRotateBytes 1048576')

if not path.exists(project_dir):
  os.makedirs(project_dir)

os.rename(src=path.join(os.getcwd(), 'start.exe'), dst=start_exe_path)

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

logging.info('Registering nodered windows task')
try: 
  register_nodered_window_task()
except Exception as err:
  logging.exception(f'Register windows task failed: {err}')
else:
  logging.info('Registering windows task successful!')

logging.info("Start ohm service")
ret = system(f'{ohmExe} start')
if not ret == 0:
  logging.exception('failed to start ohm service: {ret}')
else:
  logging.info("successfully started ohm service")
# Start ohmgraphite service
# Start nodered task

# logging.info("Installing nssm.exe...")
# try:
#   downloadNSSM(version=nssm_version)
# except Exception as err:
#   logging.exception(f"Failed to download nssm.exe: {err}")
#   sys.exit(1)
# else:
#   logging.info("Successfully installed nssm.exe")

# logging.info("Installing nodered service...")
# try:
#   install_nodered_service()
# except Exception as err:
#     logging.exception(f"Failed to install nodered service: {err}")
#     sys.exit(1)
# else:
#   logging.info("Successfully installed nodered service")

print('All services installed successfully!')

time.sleep(10)
