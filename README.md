
# aosdriver

adb(안드로이드 디버그 브릿지)를 이용해 안드로이드 디바이스를 원격제어 및 자동화할 수 있는 Wrapper를 구현합니다.

※ pure-python-adb를 이용했습니다.

## 테스트한 단말기

- Galaxy Fold
- Galaxy S20+
- Galaxy Note10

## Source Code

### aosdriver.py

구현된 기능입니다.

- ClickByXmlWait() : 화면에서 노드를 찾아 클릭합니다.
- startMainActivity() : 액티비티를 실행합니다.
- getprop() : 디바이스의 속성을 가져옵니다.

### lib.py


## 예제




## 참조

- <a href="https://pypi.org/project/pure-python-adb/">pure-python-adb(ppadb) PyPI</a>
- <a href="https://docs.python.org/ko/3/">python 문서</a>
