'''
이 코드는
1. 문장이 끝나지 않았음에도 불구하고 줄바꿈(엔터)이 되어있는 텍스트 파일을 수정한다.
2. 문장이 끝나는 것의 정의 : (" ' ? ! . ” ’) : 여기서는 이들을 문장 종결 기호라고 하겠다.*
'''

import os   # 컴퓨터 내의 파일 입출력을 위해 import함
import re   # 정규표현식(regular expression)을 사용하려고 import함
import cp949covnert


def task(file_name, encoding):  # 기존 텍스트 파일을 편집한 텍스트를 새로운 텍스트 파일에 집어 넣는 함수.
    text_file = open(file_name, 'rt', encoding=encoding)
    path, name = os.path.split(file_name)   # 파일 주소와 이름을 나누어 할당한다.
    write_file = open(path+'/edit_'+name, 'wt', encoding='UTF8')
    saved_line = ''
    final_line = ''

    # 정규 표현식 reg_exp은 (.)이 0개 이상 있으며 작은 따옴표나 큰 따옴표가 1개 있는 형식 이거나, (.)이 1개 이상 있으며 작은 따옴표나 큰 따옴표가 있거나 없는 형식을 나타낸다.
    reg_exp = re.compile(
        "([.]*('|’|\"|”)|[.]+('|’|\"|”)?)[ ]*\n")

    # 정규 표현식 reg_exp_2는 하나의 문장 종결 기호가 문장의 끝, 0개 이상의 띄어쓰기 뒤에 있는 형식을 나타낸다.
    reg_exp_2 = re.compile(".+([?]|!|[.]|'|”|\")[ ]*\n")

    # 정규 표현식 reg_exp_3는 문장 앞에 0개 이상의 띄어쓰기와 숫자 1~2개 그리고 온점이 있는 형식을 나타낸다.
    reg_exp_3 = re.compile("[ ]*[0-9]{1,2}[.].+")

    # 정규 표현식 reg_exp_4는 띄어쓰기 n개와 엔터 하나만 있는 형식을 나타낸다.
    reg_exp_4 = re.compile("[ ]*\n")

    for line in text_file.readlines():

        # 만약 현재 line이 reg_exp을(를) 만족할 경우 finla_line을 새로운 파일에 넣기 전에 이 line을 끝에 붙이고 final_line을 넣는다.
        if reg_exp.match(line):
            final_line = final_line[:-1] + line
            write_file.write(final_line)
            final_line = ''
            continue
        write_file.write(final_line)  # final_line을 새로운 파일에 넣는다.
        final_line = ''

        if line[0:4] != '    '\
                and not reg_exp_3.match(line)\
                and not reg_exp_4.match(line)\
                and not reg_exp_2.match(line):
                # if문 1번째 줄 : 띄어쓰기 4개 이상이 문장의 앞에 있는 경우 목차로 판단하여 그러지 "않을" 경우 다음 조건으로 넘긴다.(목차이면 엔터를 제거하지 않음)
                # 2번쨰 줄 : 위 조건을 만족한 문장이 reg_exp_3를 만족하지 않으면 다음 조건으로 넘긴다.
                # 3번째 줄 : 위 조건을 만족한 문장이 reg_exp_4를 만족하지 않으면 다음 조건으로 넘긴다.(엔터만 있으면 엔터를 제거하지 않음)
                # 4번째 줄 : 위 조건을 만족한 문장이 reg_exp_2를 만족하지 않으면 잘못 엔터 된 것으로 판단, 문장 끝 엔터를 제거한다.
            saved_line += line[:-1]  # 앞에 오는 문장을 편집(엔터를 제거)하여 saved_line에 넣는다.

        else:  # final_line에 편집한 문장을 넣는다.
            line = saved_line + line
            saved_line = ''
            # (")가 (??)로 바뀐 경우가 있어 밑의 두 줄을 넣었다.(평상시에는 각주처리 할 것)
            # line = line.replace('???', '?”')
            # line = line.replace("??", '”')
            # final_line에 편집한 문장을 넣어놓고 for문을 다시 시작할 때 다음 줄까지 고려 한 후 final_line을 새로운 파일에 넣을 것이다.
            final_line = line

    write_file.write(final_line)  # for문이 끝나고 마지막 final_line을 새로운 파일에 넣는다.


def text_file_edit(adress_of_file):
    for file_name in os.listdir(adress_of_file):
        if "edit_" in file_name:  # 'edit'이라는 단어가 파일 이름 앞에 있으면 이미 편집된 파일로 인식하고 건너뛴다.
            continue

        if ".txt" in file_name:  # 텍스트 파일만 인식한다.
            print(file_name)
            # 한글을 지원하는 코덱들을 하나씩 사용하며, 적용이 되면 그 코덱으로 읽고 안되면 다른 코덱을 적용해 읽는다.
            for encoding in ['utf-8', 'utf-16', 'euc-kr', 'cp949', 'iso-2022-kr', 'ksc5601', 'iso-8859-1']:
                try:
                    task(adress_of_file + file_name, encoding)
                    # 작업이 성공했음을 알리고 원본의 코덱을 알려주고 새로이 바뀐 코덱도 알려준다.
                    print(
                        f'success!(original codec : {encoding} -> new codec : utf-8)')
                    break
                except Exception as e:
                    print(f"{e}")   # 어떤 에러가 떴었는지 알려준다.
                    continue

            # 아예 안되는 경우 failed출력
            else:
                print(f'{file_name} failed')


adress = input()


# 이 함수는 텍스트 파일이 들어있는 파일의 주소를 받아 그 파일 내에 있는 텍스트 파일을 가지고 위에 써 놓은 기능을 수행하는 함수이다.
text_file_edit(adress+'/')
# 주소에 '/'를 더하는 이유는 파일 주소를 입력 했을 떄 각각의 텍스트 파일 이름 앞에 /가 붙지 않아 오류가 발생하였기 때문이다.
