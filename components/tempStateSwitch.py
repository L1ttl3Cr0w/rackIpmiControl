from components.loggingFunctions import log_data
# Single max temp when the code initializes automatic fan control
high_temp_threshold=75
low_temp_threshold=45
# Maximum combined temperature when the code initializes automatic fan control
high_combined_temp=60
# Minimum combined temperature when the code initializes manual fan control
low_combined_temp=45
# These function change the default state when the temperature thresholds are met
class temp_state:
    def __init__(self, parts, high_threshold, low_threshold, status, high_status):
        self.zero = parts[0]
        self.one = parts[1]
        self.high_temp= high_threshold
        self.low_temp = low_threshold
        self.status = status
        self.high_status = high_status
    def part_temp_state(self, part):
        if self.zero >= self.high_temp or self.one >= self.high_temp:
            log_data(__name__, "warning", f"{part} temperature is too high: {part}_zero {self.zero} ; {part}_one {self.one}")
            return True
        elif self.high_status and self.zero <= self.low_temp and self.one <= self.low_temp:
            log_data(__name__, "warning", f"{part} temperature is too high: {part}_zero {self.zero} ; {part}_one {self.one}")
            return False
        elif self.high_status:
            log_data(__name__, "warning", f"{part} temperature is too high: {part}_zero {self.zero} ; {part}_one {self.one}")
            return True
        else:
            log_data(__name__, "info", f"{part} temperature is normal: {part}_zero {self.zero} ; {part}_one {self.one}")
            return False
class combined_temp_state:
    def __init__(self, cpu, gpu, high_threshold, low_threshold, status, high_status):
        self.sum= (sum(cpu) + sum(gpu)) / len(cpu + gpu)
        self.high = high_threshold
        self.low = low_threshold
        self.status = status
        self.high_status = high_status
    def temp_state(self):
        if self.sum >= self.high:
            return True
        elif self.high_status and self.sum <= self.low:
            return False
        elif self.status:
            return True
        else:
            return False