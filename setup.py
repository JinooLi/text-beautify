from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("텍본_정리용_코드.py", base=base)]
# ‘my first prog.py’를 '텍본_정리용_코드.py'로 바꿈. 이곳에 exe파일로 바꾸고 싶은 파이썬 파일 이름을 넣으면 된다.

packages = ["idna"]
options = {
    'build_exe': {

        'packages': packages,
    },

}

setup(
    name="<any name>",
    options=options,
    version="<any number>",
    description='<any description>',
    executables=executables
)
