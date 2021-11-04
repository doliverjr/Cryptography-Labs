def pad(message, blocksize):
    paddingSize = (blocksize -len(message)) % blocksize
    if paddingSize == 0:
        paddingSize = blocksize

    padding = (chr(paddingSize) * paddingSize).encode()
    plaintext = message + padding
    return plaintext


def unpad(message, blocksize):
    if len(message)%blocksize != 0:
        raise Exception("Incorrect Pad Size")

    paddSize = message[-1]
    return message[:-paddSize]