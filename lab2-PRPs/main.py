from Crypto.Cipher import AES
from myPadding import pad, unpad
import base64
from Lab2_TaskII_A import Lab2_TaskII_A
from Lab2_TaskII_B import Lab2_TaskII_B
from Lab2_TaskII_C import Lab2_TaskII_C
from Lab2_TaskIII_A import Lab2_TaskIII_A


if __name__ == '__main__':
    print("\nRunning 2A...")
    Lab2_TaskII_A()

    print("\nRunning 2B...")
    Lab2_TaskII_B()

    print("\nRunning 2C...")
    Lab2_TaskII_C()

    print("\nRunning 3A...")
    Lab2_TaskIII_A()


