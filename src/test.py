
from aosdriver import Driver

driver = Driver()
driver.wakeup()
driver.home()
driver.startMainActivity(driver.SETTINGS_ACTIVITY_PATH)
driver.clickByXml('text', '연결')