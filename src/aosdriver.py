
from ppadb.client import Client
from xml.etree import ElementTree
import re
from queue import Queue
from time import sleep
import os


class ActivityPath:
    SETTINGS_ACTIVITY_PATH = "com.android.settings/com.android.settings.Settings"
    DIAL_ACTIVITY_PATH = "com.samsung.android.dialer/.DialtactsActivity"


class Driver:
    def __init__(self, device):
        self.device = device
        print('{}: Driver@__init__: create'.format(self.device.serial))

    def getXml(self):
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
                if cur.attrib.get(key):
                    if cur.attrib[key].strip() == value:
                        return cur
            nexts = cur.findall('node')
            for nxt in nexts:
                q.put(nxt)
        return None

    def findNodeOr(self, root, key, value=[]):
        q = Queue()
        q.put(root)
        while q.qsize():
            cur = q.get()
            if cur.tag == 'node':
                if cur.attrib.get(key):
                    for val in value:
                        if cur.attrib[key].strip() == val:
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
        self.sleep()
        return True

    def clickByXmlWaitOr(self, key, value=[]):
        print('{}: Driver@clickByXmlWaitOr: find "{}"'.format(self.device.serial, value))
        while True:
            xml = self.getXml()
            tree = ElementTree.fromstring(xml)
            node = self.findNodeOr(tree, key, value)
            if node == None:
                continue
            else:
                break
        pos = self.getBoundPos(node)
        print('{}: Driver@clickByXmlWait: click "{}"'.format(self.device.serial, value))
        self.device.shell('input tap {} {}'.format(pos[0], pos[1]))
        self.sleep()

    def clickByXmlWait(self, key, value):
        print('{}: Driver@clickByXmlWait: find "{}"'.format(self.device.serial, value))
        while True:
            xml = self.getXml()
            tree = ElementTree.fromstring(xml)
            node = self.findNode(tree, key, value)
            if node == None:
                continue
            else:
                break
        pos = self.getBoundPos(node)
        print('{}: Driver@clickByXmlWait: click "{}"'.format(self.device.serial, value))
        self.device.shell('input tap {} {}'.format(pos[0], pos[1]))
        self.sleep()


    def startMainActivity(self, path):
        print('{}: Driver@startMainActivity: start main activity {}'.format(self.device.serial, path))
        self.device.shell('am start -a android.intent.action.MAIN -n ' + path)
        self.sleep()

    def home(self):
        self.device.input_keyevent('KEYCODE_HOME')
        self.sleep()

    def menu(self):
        self.device.input_keyevent("KEYCODE_MENU")
        self.sleep()

    def wakeUp(self):
        self.device.input_keyevent('KEYCODE_WAKEUP')
        self.sleep()

    def powerBtn(self):
        self.device.input_keyevent('KEYCODE_POWER')
        self.sleep()

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
        self.sleep()            # 적당한 sleep 튜닝해야함

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
        sleep(time)

    def sleepDevice(self, time=0.1):
        self.device.shell('sleep ' + str(time))

    def sendKey(self, key=""):
        print('{}: Driver@sendKey: send '.format(self.device.serial) + key)
        self.device.shell('input text ' + key)
        self.sleep()

    def waitByXml(self):
        prev = self.getXml()
        next = prev
        print('{}: Driver@waitByXml: wait for change window'.format(self.device.serial))
        while next == prev:
            next = self.getXml()
            # sleep(0.1)

    def getprop(self, key=""):
        print('{}: Driver@getprop: get system property: {}'.format(self.device.serial, key))
        return self.device.shell('getprop {}'.format(key))

    def delete_file(self, path=""):
        # 아직 테스트 안함
        print('{}: Driver@delete_file: delete file: {}'.format(self.device.serial, path))
        self.device.shell('rm -rf {}'.format(path))
        return True

    def read_file(self, path=""):
        print('{}: Driver@read_file: read file: {}'.format(self.device.serial, path))
        content = self.device.shell('grep ".*" {}'.format(path))
        print('{}: Driver@read_file: content:\n{}'.format(self.device.serial, content))
        return content
