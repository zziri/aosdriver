
from aosdriver import *
from threading import *
from lib import *

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

lock = Lock()
count = len(drivers)


def test(driver):
    BUILD_KEY = "ro.build.version.incremental"
    # sequence
    build = driver.getprop(BUILD_KEY)
    dst = superChdir('/home/jihoon/Documents/dumpstate/{}'.format(build))
    driver.pull('/sdcard/log', dst)
    global count
    lock.acquire()
    count -= 1
    lock.release()


for driver in drivers:
    thread = Thread(target=test, args=(driver, ))
    thread.daemon = True
    thread.start()

while True:
    sleep(0.1)
    if count == 0:
        break

print('finished')