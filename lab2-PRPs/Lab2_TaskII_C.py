from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

Block_Size = 16

def ansix923_pad(plain, blocksize):
    padbytes = blocksize - len(plain) % blocksize
    plain += '\x20' * (padbytes - 1) + chr(padbytes)
    return plain


def getNewKey():
    answer = "d73c08ebfeae19c1f13e7e8af4b48e15645fe85169c7c8c25535f1eefa8ec013814629b1eb10841c9ea7753eb151d7cd645fe85169c7c8c25535f1eefa8ec013"
    hexbytes = bytes.fromhex(answer)
    chunks2 = [1,2,3,4]
    chunks = [hexbytes[i:i + 16] for i in range(0, len(hexbytes), 16)]

    chunks2[0] =chunks[0]
    chunks2[1] =chunks[1]
    chunks2[2] = chunks[2]
    chunks2[3] = chunks[1]

    back = b''.join(chunks2)
    print(chunks)
    print(back.hex())


def Lab2_TaskII_C():
    admin = ansix923_pad("admin", Block_Size)
    uname = 'zzzzzzzzzzz' + admin + 'zzzz'
    print(uname)




