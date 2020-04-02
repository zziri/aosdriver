
from ppadb.client import Client
from xml.etree import ElementTree
import os
import re
from queue import Queue


class ActivityPath:
    SETTINGS_ACTIVITY_PATH = "com.android.settings/com.android.settings.Settings"


class Driver:
    def __init__(self, host='127.0.0.1', port=5037):
        client = Client(host, port)
        self.waitForDevice()
        self.devices = client.devices()
        print('Driver@__init__: start driver')

    def waitForDevice(self):
        print('Driver@waitForDevice: waiting for devices...')
        os.popen('adb wait-for-device').read()  # read() 해줘야 대기함

    def getXml(self, device):
        # path 가져와서 할 것 추가해야함
        str = device.shell('uiautomator dump')
        path = '/sdcard/window_dump.xml'
        return device.shell('cat ' + path)

    # 테스트 필요
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

    # 위에 함수로 대체할 것임
    # def findNode(self, tree, key, value):
    #     q = list()
    #     q.append(tree)
    #     while q:
    #         cur = q.pop(0)
    #         if cur.tag == 'node':
    #             if cur.attrib[key] == value:
    #                 return cur
    #         nexts = cur.findall('node')
    #         for nxt in nexts:
    #             q.append(nxt)
    #     return None

    def getBoundPos(self, node):
        ret = []
        pos = re.findall('\d+', node.attrib['bounds'])
        ret.append(int((int(pos[0]) + int(pos[2])) / 2))
        ret.append(int((int(pos[1]) + int(pos[3])) / 2))
        return ret

    def clickByXml(self, key, value):
        for device in self.devices:
            # xml dump
            xml = self.getXml(device)
            # make tree
            tree = ElementTree.fromstring(xml)
            # find node
            node = self.findNode(tree, key, value)
            if node == None:
                return False
            # find position
            pos = self.getBoundPos(node)
            # touch
            device.shell('input tap {} {}'.format(pos[0], pos[1]))

        return True

    def startMainActivity(self, path):
        for device in self.devices:
            str = device.shell('am start -a android.intent.action.MAIN -n ' + path)
            print(device.serial + ': ' + str)

    def home(self):
        for device in self.devices:
            device.shell('input keyevent KEYCODE_HOME')

    def wakeup(self):
        for device in self.devices:
            device.shell('input keyevent KEYCODE_WAKEUP')

    def pageDownScroll(self):       # 개발 전
        print('Driver@pageDownScroll: page down start')

    def dumpstate(self):            # 개발 전
        print('Driver@dumpstate: dumpstate start')
        
    def sleep(self, time=0.1):
        print('Driver@sleep: sleep ' + str(time))
        for device in self.devices:
            device.shell('sleep ' + str(time))

    def sendKey(self, key=""):
        print('Driver@sendKey: send ' + key)
        for device in self.devices:
            device.shell('input text ' + key)




