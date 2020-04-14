
from ppadb.client import Client
import os


def getDevices(host='127.0.0.1', port=5037):
    client = Client(host, port)
    waitForDevice()
    return client.devices()


def waitForDevice():
    print('aosdriver@waitForDevice: waiting for devices...')
    os.popen('adb wait-for-device').read()  # read() 해줘야 대기함