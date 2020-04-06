
from aosdriver import *

DESTINATION_PATH = "/home/jihoon/Documents/klog/fastdumpstate.lst"
driver = Driver()
driver.wakeup()
paths = driver.dumpstate()
path = paths[0]
driver.pull(path, DESTINATION_PATH)
