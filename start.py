from os import path, system
import os

import logging

logging.getLogger(__name__)


project_dir = 'C:\powerlytics'
ohm_path = path.join(project_dir, "OhmGraphite.exe")
nssm_path = path.join(project_dir, "nssm.exe")
powerlytics_service = "powerlytics"

logging.basicConfig(level='INFO', filename=f'{project_dir}/logs.txt', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
os.chdir(project_dir)

start_services_cmd = f'{ohm_path} start && {nssm_path} start {powerlytics_service}'

ret = system(start_services_cmd)

if not ret==0:
    logging.exception(f'Failed to start all services with code {ret}')
logging.info('All services started, please go to http://localhost:1880')