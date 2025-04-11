import time
import components.callTemperature as callTemp
import components.systemControl as sysCon
from components.loggingFunctions import log_data
# Fan speed that you are comfortable to use
fan_speed=30
# Starting default values of states
cpu_status = False
gpu_status = False
combined_status = False
high_status = False
if __name__ == '__main__':
    while True:
        print(f"Code start current high_status: {high_status}")
        time.sleep(2)
        status = sysCon.check_system_state(cpu_temp = callTemp.call_cpu_temp(), gpu_temp =callTemp.call_gpu_temp(), cpu_status = cpu_status, gpu_status = gpu_status, combined_status = combined_status, high_status = high_status)
        if status != None:
            if status[0] or status[1] or status[2]:
                high_status = sysCon.system_high_state(status, high_status)
            else:
                high_status = sysCon.system_low_state(high_status, fan_speed)
        else:
            log_data(__name__, 'critical', 'Program failure, one or more components failed in retrieving data, please manually check the system for status')
        print(f'code end 2s sleep. Current high_status: {high_status}')
        time.sleep(2)