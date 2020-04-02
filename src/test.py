
from aosdriver import Driver
from aosdriver import ActivityPath

driver = Driver()
driver.wakeup()
driver.home()
driver.startMainActivity(ActivityPath.SETTINGS_ACTIVITY_PATH)
driver.clickByXml('text', '연결')