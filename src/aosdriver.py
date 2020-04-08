
from ppadb.client import Client
from xml.etree import ElementTree
import os
import re
from queue import Queue
from time import sleep


def getDevices(host='127.0.0.1', port=5037):
    client = Client(host, port)
    waitForDevice()
    return client.devices()

def waitForDevice():
    print('aosdriver@waitForDevice: waiting for devices...')
    os.popen('adb wait-for-device').read()  # read() 해줘야 대기함


class ActivityPath:
    SETTINGS_ACTIVITY_PATH = "com.android.settings/com.android.settings.Settings"
    CCICLPM_ACTIVITY_PATH = "com.sec.android.app.factorykeystring/com.sec.android.app.status.CCIC_LPM"
    SYSDUMP_ACTIVITY_PATH = "com.sec.android.app.servicemodeapp/.SysDump"
    DIAL_ACTIVITY_PATH = "com.samsung.android.dialer/.DialtactsActivity"


class Driver:
    def __init__(self, device):
        self.device = device
        print('{}: Driver@__init__: create'.format(self.device.serial))

    def getXml(self):
        # path 가져와서 할 것 추가해야함
        words = self.device.shell('uiautomator dump')
        path = ""
        words = words.split(' ')
        for word in words:
            if '.xml' in word:
                path = word
                break
        return self.device.shell('cat ' + path)

    def findNode(self, root, key, value):
        q = Queue()
        q.put(root)
        while q.qsize():
            cur = q.get()
            if cur.tag == 'node':
                if cur.attrib[key] == value:
                    return cur
            nexts = cur.findall('node')
            for nxt in nexts:
                q.put(nxt)
        return None

    def getBoundPos(self, node):
        ret = []
        pos = re.findall('\d+', node.attrib['bounds'])
        ret.append(int((int(pos[0]) + int(pos[2])) / 2))
        ret.append(int((int(pos[1]) + int(pos[3])) / 2))
        return ret

    def clickByXml(self, key, value):
        print('{}: Driver@clickByXml: click "{}"'.format(self.device.serial, value))
        # xml dump
        xml = self.getXml()
        # make tree
        tree = ElementTree.fromstring(xml)
        # find node
        node = self.findNode(tree, key, value)
        if node == None:
            return False
        # find position
        pos = self.getBoundPos(node)
        # touch
        self.device.shell('input tap {} {}'.format(pos[0], pos[1]))
        return True

    def startMainActivity(self, path):
        str = self.device.shell('am start -a android.intent.action.MAIN -n ' + path)
        print(self.device.serial + ': ' + str)

    def home(self):
        self.device.input_keyevent('KEYCODE_HOME')
        # self.device.shell('input keyevent KEYCODE_HOME')

    def wakeUp(self):
        self.device.input_keyevent('KEYCODE_WAKEUP')

    def powerBtn(self):
        self.device.input_keyevent('KEYCODE_POWER')

    def pageDownScroll(self):       # 튜닝 전
        print('{}: Driver@pageDownScroll: page down start'.format(self.device.serial))
        # set start, end pos
        size = self.device.wm_size()
        start_x = int(size.width/2)
        start_y = int(size.height*0.7)
        end_x = start_x
        end_y = int(size.height*0.3)
        # swipe
        self.device.input_swipe(start_x, start_y, end_x, end_y, 1000)

    def findLogPath(self, dumpLog=""):
        logs = dumpLog.split('\n')
        for log in logs:
            if "Log path:" in log:
                log = log.split(' ')
                for word in log:
                    if ".txt" in word:
                        return word
        return ""

    def dumpstate(self):            # 테스트 전
        print('{}: Driver@dumpstate: dumpstate start'.format(self.device.serial))
        dumpLog = self.device.shell('dumpstate')
        return self.findLogPath(dumpLog)

    def pull(self, src, dst):
        print('{}: Driver@pull: pull from '.format(self.device.serial) + src + ' to ' + dst)
        os.popen('adb -s {} pull {} {}'.format(self.device.serial, src, dst)).read()

    def sleep(self, time=0.1):
        print('{}: Driver@sleep: sleep '.format(self.device.serial) + str(time))
        self.device.shell('sleep ' + str(time))

    def sendKey(self, key=""):
        print('{}: Driver@sendKey: send '.format(self.device.serial) + key)
        self.device.shell('input text ' + key)

    def waitByXml(self):
        prev = self.getXml()
        next = prev
        print('{}: Driver@waitByXml: wait for change window'.format(self.device.serial))
        while next == prev:
            next = self.getXml()
            sleep(0.5)




