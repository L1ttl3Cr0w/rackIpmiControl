import time
import components.callTemperature as callTemp
import components.systemControl as sysCon
from components.logDataFormat import logging_data
# Fan speed that you are comfortable to use
fan_speed=15
# Starting default values of states
cpu_status = False
gpu_status = False
combined_status = False
high_status = False
gpu_installed = False
mongoDB = True
if __name__ == '__main__':
    while True:
        time.sleep(2)
        status = sysCon.check_system_state(callTemp.call_cpu_temp(mongoDB), callTemp.call_gpu_temp(gpu_installed, mongoDB), cpu_status, gpu_status, combined_status, high_status, mongoDB)
        if status != None:
            if status[0] or status[1] or status[2]:
                high_status = sysCon.system_high_state(status, high_status, mongoDB)
            else:
                high_status = sysCon.system_low_state(high_status, fan_speed, mongoDB)
        else:
            logging_data(__name__, 'critical', 'Program failure, one or more components failed in retrieving data, please manually check the system for status', mongoDB)
        time.sleep(2)