import os
import re


def cp949toUTF8(path):
    # Open input file
    with open(path, 'rb') as fi:
        # Open output file
        with open(path[0:-4]+'_edit.txt', 'wb') as fo:

            # Read all lines
            while True:

                # Read until EOF
                line = fi.readline()
                if len(line) == 0:
                    break

                # Try to convert whole line
                try:
                    fo.write(line.decode('cp949').encode('utf-8'))

                # If it fails, convert letter by letter
                except:
                    i = 0
                    while i < len(line):
                        try:
                            # Double-byte
                            fo.write(
                                line[i:i+2].decode('cp949').encode('utf-8'))
                        except:
                            try:
                                # Single-byte
                                fo.write(
                                    line[i:i+1].decode('cp949').encode('utf-8'))
                            except:
                                # ERR
                                fo.write('�'.encode('utf-8'))
                            i -= 1
                            pass
                        i += 2


if __name__ == '__main__':
    cp949toUTF8(r'C:\Users\jinu1\Downloads\이영도 소설\드래곤라자 1~15 [완] - 이영도-1.txt')
    # print(bytearray([63, 177]).decode('cp949'))
