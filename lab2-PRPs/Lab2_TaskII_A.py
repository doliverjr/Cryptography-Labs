import base64
from myPadding import pad, unpad
from Crypto.Cipher import AES

Block_Size = 16
key1 = "CALIFORNIA LOVE!"

def ecb_decrypt(key, ciphertext):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decoded = cipher.decrypt(ciphertext)
    message = unpad(decoded, Block_Size)
    return message.decode()

def ecb_encrypt(key, message):
    plaintext = pad(message, Block_Size)
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return cipher.encrypt(plaintext)

def decodeFromFile64(text):
    ciphertext = base64.b64decode(text)
    decoded = ecb_decrypt(key1, ciphertext)
    return decoded

def Lab2_TaskII_A():
    file = open("Lab2.TaskII.A.txt", "rb")
    text = decodeFromFile64(file.read())
    print(f'{text}')