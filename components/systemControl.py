import os
import subprocess
from components.tempStateSwitch import temp_state, combined_temp_state
from components.logDataFormat import logging_data
def system_high_state(state, high_status):
    try:
        if high_status == False:
            if state != None:
                for value in state:
                    if value:
                        # This ipmi code here sets the fans into automatic mode
                        subprocess.run(['ipmitool', 'raw', '0x30', '0x30', '0x01', '0x01'])
                        logging_data(__name__, 'warning', 'One of the system components is to hot, starting automatic fan control')
                        return True
            else:
                logging_data(__name__, 'error', 'States registered as none, failure in one of the fetch functions')
                return True
        elif high_status:
            logging_data(__name__, 'info', 'System already in high state skipping ipmi')
            return True
        else:
            logging_data(__name__, 'error', 'Failure in system high state, high_status was not returned as boolean')
            return True
    except Exception as e:
        logging_data(__name__, 'error', f'Failed to set server rack fans into automatic mode. Error: {e}')
        return None
def system_low_state(high_status, fan_speed):
    try:
        if high_status:
            # This ipmi code here sets the server rack fans into manual mode        
            subprocess.run(['ipmitool', 'raw', '0x30', '0x30', '0x01', '0x00'])
            # This ipmi code here sets the fan speed (fan_speed)
            subprocess.run(['ipmitool', 'raw', '0x30', '0x30', '0x02', '0xff', hex(fan_speed)])
            logging_data(__name__, 'info', f'Fan control has been set back into manual mode: manua; fan speed: {fan_speed}%')
            return False
        else:
            logging_data(__name__, 'info', f'Fan control is already set to manual skipping ipmitool instructions. Default fan speed in manual mode: {fan_speed}%')
            return False
    except Exception as e:
        logging_data(__name__, 'error', f'An error happened trying to change speed of the fans. Error:{e}')
        return None

def check_system_state(cpu_temp, gpu_temp, cpu_status, gpu_status, combined_status, high_status):
    cpu = temp_state(parts = cpu_temp, high_threshold = 75, low_threshold = 45, status = cpu_status, high_status = high_status)
    gpu = temp_state(parts = gpu_temp, high_threshold = 75, low_threshold = 45, status = gpu_status, high_status = high_status)
    combined = combined_temp_state(cpu = cpu_temp, gpu = gpu_temp, high_threshold = 60, low_threshold = 45, status = combined_status, high_status = high_status)
    states = [cpu.part_temp_state('cpu'), gpu.part_temp_state('gpu'), combined.temp_state()]
    for value in states:
        if type(value) != bool:
            logging_data(__name__, 'error', f'Failure in obtaining value from temp state switch component, manual setting automatic fan control')
            return None
    else:
        logging_data(__name__, 'info', 'Value obtained from state switch module without failure')
        return states