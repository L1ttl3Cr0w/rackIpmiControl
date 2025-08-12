import signal
import subprocess
from components.logDataFormat import logging_data

class SignalHandler:
    shutdown_requested = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)
    def request_shutdown(self, mongodb):
        print("Request for shutdown recieved, stopping service.")
        self.shutdown_requested = True
        subprocess.run(['ipmitool', 'raw', '0x30', '0x30', '0x01', '0x01'])
        logging_data(__name__, 'critical', 'Activating automatic ipmi control, python program failure, terminating process', mongodb)
        subprocess.run(['systemctl', 'stop', 'pythoncontrol.service'])
    def can_run(self):
        return not self.shutdown_requested
    