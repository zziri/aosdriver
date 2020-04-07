
from aosdriver import *
from threading import *

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

lock = Lock()
count = len(drivers)


def fulldumpstate(driver):
    global count
    # sequence
    driver.wakeUp()
    driver.home()
    driver.startMainActivity(ActivityPath.DIAL_ACTIVITY_PATH), driver.sleep()
    driver.clickByXml('resource-id', "com.samsung.android.dialer:id/dialpad_tab_button"), driver.sleep()
    driver.sendKey('*#9900#'), driver.sleep()
    driver.clickByXml('text', 'Run dumpstate/logcat'), driver.sleep()
    driver.waitByXml()
    driver.clickByXml('text', 'OK'), driver.sleep()
    driver.clickByXml('text', 'Copy to sdcard(include CP Ramdump)'), driver.sleep()
    driver.waitByXml()
    driver.clickByXml('text', 'OK')
    driver.pull('/sdcard/log', '/home/jihoon/Documents/klog/autodumpstate/')
    driver.home()

    lock.acquire()
    count -= 1
    lock.release()


for driver in drivers:
    thread = Thread(target=fulldumpstate, args=(driver, ))
    thread.daemon = True
    thread.start()

while True:
    if count == 0:
        break

print('finished')
