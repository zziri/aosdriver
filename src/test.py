
from aosdriver import *

client = Client()
devices = client.devices()
driver = Driver(devices[0])

print(driver.getXml())