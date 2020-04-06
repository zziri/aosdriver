
from aosdriver import Driver
from aosdriver import ActivityPath

driver = Driver()
driver.wakeup()
paths = driver.dumpstate()
print(paths)
driver.pull(paths[0], '/home/jihoon/Documents/klog/fastdumpstate.lst')
