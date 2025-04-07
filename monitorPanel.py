import time
import components.callTemperature as callTemp
import components.tempStateSwitch as switch
# Fan speed that you are comfortable to use
fan_speed=30
def system_high_state():
    print("A subprocess is going to be run here to set the fan speed to automatic")
def system_low_state():
    print("A subprocess is going to be run here to set the fan to manual mode and set the manual speed")
print("Starting monitoring, before any value insert there's going to be a one second delay to check if the data obtained is fast enough")
while True:
    time.sleep(2)
    cpu_temp_zero, cpu_temp_one = callTemp.call_cpu_temp()
    gpu_temp_zero, gpu_temp_one = callTemp.call_gpu_temp()
    combined_temp = callTemp.call_combined_temp(cpu_temp_zero, cpu_temp_one, gpu_temp_zero, gpu_temp_one)
    cpu_status = switch.cpu_temp_state(cpu_temp_zero, cpu_temp_one)
    gpu_status = switch.gpu_temp_state(gpu_temp_zero, gpu_temp_one)
    combined_status = switch.combined_temp_state(combined_temp)
    if gpu_status or cpu_status or combined_status:
        system_high_state()
        time.sleep(2)
    else:
        system_low_state()
        time.sleep(5)