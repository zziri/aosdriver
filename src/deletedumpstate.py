
from aosdriver import *
from threading import *
from lib import *

devices = getDevices()
drivers = []
for device in devices:
    drivers.append(Driver(device))

lock = Lock()
count = len(drivers)


def deldumpstate(driver):
    # sequence
    driver.wakeUp()
    driver.menu()
    driver.home()
    driver.startMainActivity(ActivityPath.DIAL_ACTIVITY_PATH)
    driver.clickByXmlWait('resource-id', "com.samsung.android.dialer:id/dialpad_tab_button")
    driver.sendKey('*#9900#')
    driver.clickByXmlWait('text', 'Delete dumpstate/logcat')
    # driver.clickByXmlWait('text', 'OK')
    driver.clickByXmlWaitOr('text', ['OK', '확인'])
    driver.home(), driver.home()
    driver.powerBtn()
    # critical section
    global count
    lock.acquire()
    count -= 1
    lock.release()


for driver in drivers:
    thread = Thread(target=deldumpstate, args=(driver, ))
    thread.daemon = True
    thread.start()
# spin lock
while True:
    sleep(0.1)
    if count == 0:
        break

print('delete dumpstate finished')
