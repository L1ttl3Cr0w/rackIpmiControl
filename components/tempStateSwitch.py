from components.logDataFormat import logging_data
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
        self.parts = parts
        self.high_temp= high_threshold
        self.low_temp = low_threshold
        self.status = status
        self.high_status = high_status
    def part_temp_state(self, part):
        try:
            if type(self.parts) == list:
                if any(part >= self.high_temp for part in self.parts) == True:
                    return True
                elif self.high_status and any(part <= self.low_temp for part in self.parts):
                    return False
                elif self.high_status:
                    return True
                else: 
                    return False
            else:
                if self.parts >= self.high_temp:
                    return True
                elif self.high_status and self.parts <= self.low_temp:
                    return False
                elif self.high_status:
                    return True
                else: 
                    return False
        except Exception as e:
            return None
class combined_temp_state:
    def __init__(self, cpu, gpu, high_threshold, low_threshold, status, high_status):
        if gpu == 0:
            self.sum = sum(cpu) / len(cpu)
        elif type(gpu) != list:
            self.sum = gpu + sum(cpu) / (len(cpu) + 1)
        elif cpu == None:
            self.sum = sum(gpu) / len(gpu)
        else:
            self.sum = (sum(gpu) + sum(cpu)) / len(cpu + gpu)
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