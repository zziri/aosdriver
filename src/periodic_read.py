from aosdriver import *
from lib import *
from time import time

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

driver = drivers[0]

file_path = "/home/jihoon/Documents/temp/result.csv"
logs = list()
logs.append("time, policy0, policy4, policy7")
start = int(round(time() * 1000))
freqs = [0] * 3


def get_time():
    return int(round(time() * 1000)) - start


print("loop start")

while True:
    try:
        freqs[0] = driver.read_file("/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq").rstrip()
        freqs[1] = driver.read_file("/sys/devices/system/cpu/cpufreq/policy4/scaling_cur_freq").rstrip()
        freqs[2] = driver.read_file("/sys/devices/system/cpu/cpufreq/policy7/scaling_cur_freq").rstrip()
        logs.append("{}, {}, {}, {}".format(
            get_time(),
            freqs[0],
            freqs[1],
            freqs[2]
        ))
    except KeyboardInterrupt:
        print("\ncomplete")
        break
    except Exception as e:
        break

with open(file_path, "w") as file:
    for log in logs:
        file.write("{}\n".format(log))
