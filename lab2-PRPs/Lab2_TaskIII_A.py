from Crypto.Cipher import AES
from myPadding import pad, unpad
import base64

Block_Size = 16
key2 = "MIND ON MY MONEY"
IV = "MONEY ON MY MIND"

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def cbc_encrypt(message, key, IV):
    plaintext = pad(message, Block_Size)
    numBlocks = int(len(plaintext) / Block_Size)
    ciphertext = b''

    cipher = AES.new(key.encode(), AES.MODE_ECB)
    IVPad = IV.encode()
    output = IVPad

    for i in range(numBlocks):
        startBlock = i*Block_Size
        input = byte_xor(output, plaintext[startBlock : startBlock+Block_Size])
        output = cipher.encrypt(input)
        ciphertext += output

    return IVPad + ciphertext

def cbc_decrypt(ciphertext, key, IV):
    plaintext = b''
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    ciphertext = ciphertext[len(IV.encode()):]
    numBlocks = int(len(ciphertext) / Block_Size)

    postDecrypt = cipher.decrypt(ciphertext[:Block_Size])
    output = byte_xor(postDecrypt, IV.encode())
    plaintext += output
    previous = ciphertext[:Block_Size]


    for i in range(1, numBlocks):
        startBlock = i*Block_Size
        preDecrypt = ciphertext[startBlock : startBlock+Block_Size]
        postDecrypt = cipher.decrypt(preDecrypt)
        output = byte_xor(postDecrypt, previous)
        previous = preDecrypt

        plaintext += output

    return unpad(plaintext, Block_Size)

def decodeFromFile64(text):
    ciphertext = base64.b64decode(text)
    decoded = cbc_decrypt(ciphertext, key2, IV)
    return decoded

def Lab2_TaskIII_A():
    file = open("Lab2.TaskIII.A.txt", "rb")
    cipherText = file.read()
    text = decodeFromFile64(cipherText)
    print(f'{text.decode()}')