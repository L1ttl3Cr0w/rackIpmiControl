import os
import subprocess
from components.loggingFunctions import log_data
from dotenv import load_dotenv
load_dotenv()
def call_cpu_temp():
    try:
        #call_system_temp_table = subprocess.check_output(['ipmitool', '-I', 'lanplus', '-H', os.getenv("ipmi_host"), '-U', os.getenv("ipmi_user"), '-P', os.getenv("ipmi_passwd"), '-y', os.getenv("ipmi_ekey"), '-L', os.getenv("operator_type"), 'sdr', 'type', 'temperature']).decode()
        call_system_temp_table = subprocess.check_output(['ipmitool', 'sdr', 'type', 'temperature']).decode()
        cpu_temp_zero  = int(call_system_temp_table.split('Temp')[3].strip().split()[7])
        cpu_temp_one = int(call_system_temp_table.split('Temp')[4].strip().split()[7])
    except Exception as e:
        log_data(__name__, "error", f"Error calling CPU temperature: {e}")
        return None
    finally:
        log_data(__name__, 'info', f'CPU temperature call was successful: cpu_zero {cpu_temp_zero} C, cpu_one {cpu_temp_one} C')
        return cpu_temp_zero, cpu_temp_one
def call_gpu_temp():
    try:
        gpu_temp_zero = int(subprocess.check_output(['nvidia-smi', '-i', '0', '--query-gpu=temperature.gpu', '--format=csv,noheader']).decode().strip())
        gpu_temp_one = int(subprocess.check_output(['nvidia-smi', '-i', '1', '--query-gpu=temperature.gpu', '--format=csv,noheader']).decode().strip())
    except Exception as e:
        log_data(__name__, "error", f"Error calling GPU temperature: {e}")
        return None
    finally:
        log_data(__name__, 'info', f'GPU temperature call was successful: gpu_zero {gpu_temp_zero} C, gpu_one {gpu_temp_one} C')
        return gpu_temp_zero, gpu_temp_one
def call_combined_temp(cpu_temp_zero, cpu_temp_one, gpu_temp_zero, gpu_temp_one):
    try:
        combined_temp = (cpu_temp_zero + cpu_temp_one + gpu_temp_zero + gpu_temp_one) / 4
    except Exception as e:
        log_data(__name__, "error", f"Erorr calculating combined temperature. Error:{e}")
        return None
    else:
        log_data(__name__, "info", f"Combined temperature is: {combined_temp}")
        return combined_temp