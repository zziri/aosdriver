
import os
try:
    import ppadb.client
except:
    print(os.popen('pip install pure-python-adb').read())

print('ppadb imported')