
from ppadb.client import Client
import os


def getDevices(host='127.0.0.1', port=5037):
    client = Client(host, port)
    waitForDevice()
    return client.devices()


def waitForDevice():
    print('aosdriver@waitForDevice: waiting for devices...')
    os.popen('adb wait-for-device').read()  # read() 해줘야 대기함


def superChdir(dst=""):
    dst = dst.strip()
    if os.path.isdir(dst):
        return dst
    dst = dst.replace('/', ' ')
    dst = dst.strip(' ')
    dirlist = dst.split(' ')
    os.chdir('/')
    for dir in dirlist:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        os.chdir(dir)
    return os.getcwd().strip()

