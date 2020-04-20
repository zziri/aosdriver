
from aosdriver import *
from threading import *
from lib import *

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

lock = Lock()
count = len(drivers)


def fulldumpstate(driver):
    BUILD_KEY = "ro.build.version.incremental"
    # sequence
    global count
    driver.wakeUp()
    driver.home()
    driver.startMainActivity(ActivityPath.DIAL_ACTIVITY_PATH)
    driver.clickByXmlWait('resource-id', "com.samsung.android.dialer:id/dialpad_tab_button")
    driver.sendKey('*#9900#')
    driver.clickByXmlWait('text', 'Run dumpstate/logcat')
    driver.clickByXmlWait('text', 'OK')
    driver.clickByXmlWait('text', 'Copy to sdcard(include CP Ramdump)')
    driver.clickByXmlWait('text', 'OK')
    build = driver.getprop(BUILD_KEY)
    dst = superChdir('~/Documents/dumpstate/{}'.format(build))
    src = '/sdcard/log'
    driver.pull(src, dst)
    driver.home(), driver.home()
    driver.powerBtn()

    lock.acquire()
    count -= 1
    lock.release()


for driver in drivers:
    thread = Thread(target=fulldumpstate, args=(driver, ))
    thread.daemon = True
    thread.start()

while True:
    sleep(0.1)
    if count == 0:
        break

print('finished')
