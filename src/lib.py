
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
    # 양 옆 공백을 지웁니다
    dst = dst.strip()
    # 디렉토리가 있는지 확인하고 있으면 그대로 반환합니다
    if os.path.isdir(dst):
        return dst
    # 문자'/'를 지우고 공백으로 대체합니다
    dst = dst.replace('/', ' ')
    # 양 옆 공백을 지웁니다
    dst = dst.strip(' ')
    # 공백을 기준으로 문자열을 나눕니다
    dirlist = dst.split(' ')
    # 루트 디렉토리로 이동합니다
    os.chdir('/')
    for dir in dirlist:
        # '~' = /home/<user name> 디렉토리로 이동합니다
        if dir is '~':
            os.chdir(os.popen('cd ~; pwd').read().strip())
            continue
        # 디렉토리가 존재하지 않으면 디렉토리를 만듭니다
        if not os.path.isdir(dir):
            os.mkdir(dir)
        # 디렉토리로 이동합니다
        os.chdir(dir)
    # 이동 완료한 현재 디렉토리의 경로를 반환합니다, 공백(개행문자)를 지워서 반환합니다
    return os.getcwd().strip()

