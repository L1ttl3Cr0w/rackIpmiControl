import time
import components.callTemperature as callTemp
import components.systemControl as sysCon
from components.signalHandler import SignalHandler
from components.logDataFormat import logging_data
signal_handler = SignalHandler()
# Fan speed that you are comfortable to use
fan_speed=15
# Starting default values of states
gpu_installed = True
mongoDB = False
debug = True
class system_status_table:
    def __init__(self):
        self.cpu_status = False
        self.gpu_status = False
        self.combined_status = False
        self.high_status = False
    def change_states(self, list: list):
        if len(list) == 3:
            self.cpu_status = list[0]
            self.gpu_status = list[1]
            self.combined_status = list[2]
if __name__ == '__main__':
    systemStatus = system_status_table()
    while signal_handler.can_run():
        time.sleep(2)
        status = sysCon.check_system_state(callTemp.call_cpu_temp(mongoDB, debug), callTemp.call_gpu_temp(gpu_installed, mongoDB, debug), systemStatus.cpu_status, systemStatus.gpu_status, systemStatus.combined_status, systemStatus.high_status, mongoDB)
        systemStatus.change_states(status)
        if status != None:
            if any(state for state in status):
                systemStatus.high_status = sysCon.system_high_state(status, systemStatus.high_status, mongoDB)
            else:
                systemStatus.high_status = sysCon.system_low_state(systemStatus.high_status, fan_speed, mongoDB)
        else:
            logging_data(__name__, 'critical', 'Program failure, one or more components failed in retrieving data, please manually check the system for status', mongoDB)
        time.sleep(2)