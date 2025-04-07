from components.loggingFunctions import log_data
# Default states for the temperature statuses
combined_high_status = False
cpu_high_status = False
gpu_high_status = False
# Single max temp when the code initializes automatic fan control
high_temp_threshold=75
low_temp_threshold=45
# Maximum combined temperature when the code initializes automatic fan control
high_combined_temp=60
# Minimum combined temperature when the code initializes manual fan control
low_combined_temp=45
# These function change the default state when the temperature thresholds are met
def cpu_temp_state(cpu_temp_zero, cpu_temp_one):
    global cpu_high_status
    if cpu_temp_zero >= high_temp_threshold or cpu_temp_one >= high_temp_threshold:
        cpu_high_status = True
        log_data(__name__, "warning", f"CPU temperature is too high: cpu_zero {cpu_temp_zero} ; cpu_one {cpu_temp_one}")
        return cpu_high_status
    elif cpu_high_status and cpu_temp_zero <= low_temp_threshold and cpu_temp_one <= low_temp_threshold:
        cpu_high_status = False
        log_data(__name__, "info", f"CPU temperature is back to normal: cpu_zero {cpu_temp_zero} ; cpu_one {cpu_temp_one}")
        return cpu_high_status
    else:
       log_data(__name__, "info", f"CPU state has not changed. Cpu temp: cpu_zero {cpu_temp_zero} ; cpu_one {cpu_temp_one}")
       return cpu_high_status
def gpu_temp_state(gpu_temp_zero, gpu_temp_one):
    global gpu_high_status
    if gpu_temp_zero >= high_temp_threshold or gpu_temp_one >= high_temp_threshold:
        gpu_high_status = True
        log_data(__name__, "warning", f"GPU temperature is too high: {gpu_temp_zero} or {gpu_temp_one}")
        return gpu_high_status
    elif gpu_high_status and gpu_temp_zero <= low_temp_threshold and gpu_temp_one <= low_temp_threshold:
        gpu_high_status = False
        log_data(__name__, "info", f"GPU temperature is back to normal: {gpu_temp_zero} and {gpu_temp_one}")
        return gpu_high_status
    else:
        log_data(__name__, "info", f"GPU state has not changed. GPUs temp: {gpu_temp_zero} and {gpu_temp_one}")
        return gpu_high_status
def combined_temp_state(combined_temp):
    global combined_high_status
    if combined_temp >= high_combined_temp:
        combined_high_status = True
        log_data(__name__, "warning", f"Combined temperature is too high: {combined_temp}")
        return combined_high_status
    elif combined_high_status and combined_temp <= low_combined_temp:
        combined_high_status = False
        log_data(__name__, "info", f"Combined temperature is back to normal: {combined_temp}")
        return combined_high_status
    else:
        log_data(__name__, "info", f"Combined state has not changed. Combined temp: {combined_temp}")
        return combined_high_status