

from aosdriver import *
from threading import *
from lib import *
import sys

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

driver = drivers[0]

while True:
    driver.read_file(sys.argv[1])
    sleep(1)

# "/sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq"
