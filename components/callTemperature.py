import os
import subprocess
from components.logDataFormat import logging_data
from dotenv import load_dotenv
load_dotenv()
def call_cpu_temp(mongoDB, debug):
    try:
        if debug:
            cpu_temp_one = 35
            cpu_temp_zero = 35
        else:
            call_system_temp_table = subprocess.check_output(['ipmitool', 'sdr', 'type', 'temperature'], encoding="utf-8")
            cpu_temp_zero  = int(call_system_temp_table.split('Temp')[3].strip().split()[7])
            cpu_temp_one = int(call_system_temp_table.split('Temp')[4].strip().split()[7])
    except Exception as e:
        logging_data(__name__, "error", f"Error calling CPU temperature: {e}", mongoDB)
        return None
    else:
        logging_data(__name__, 'info', f'CPU temperature call was successful: cpu_zero {cpu_temp_zero} C, cpu_one {cpu_temp_one} C', mongoDB)
        return [cpu_temp_zero, cpu_temp_one]
def call_gpu_temp(gpu_installed, mongoDB, debug):
    try:
        if debug:
            gpu_call = 35
        else:
            gpu_call = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"], encoding="utf-8").splitlines()
            if type(gpu_call) == list:
                gpu_call = list(map(int, gpu_call))
            else:
                gpu_call = int(gpu_call)
    except Exception as e:
        if gpu_installed == True:
            logging_data(__name__, "error", f"Error calling GPU temperature: {e}", mongoDB)
        else:
            logging_data(__name__, "info", f"No gpu was installed with user input", mongoDB)
        gpu_call = 0
        return gpu_call
    else:
        logging_data(__name__, 'info', f'GPU temperature call was successful: temp array: {gpu_call}', mongoDB)
        return gpu_call