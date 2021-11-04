import ConvertASCII
from string import printable
from itertools import cycle
from base64 import b64decode


def xor_string(message, key):
    encrypt = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(key)))
    return encrypt


def partA():
    print("Running Part A\n    Message: PyCharm\n    Key: no")
    encrypt = xor_string('PyCharm', 'no')
    print("    Encrypted code in hex: {}".format(ConvertASCII.ConvertToHex(encrypt)))
    print("    Decrypted: {}".format(xor_string(encrypt, 'no')))


def score_english(message):
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }

    return sum([character_frequencies.get(chr(byte), 0) for byte in message.lower()])


def single_char_xor_helper(message, key):
    return bytes([b ^ key for b in message])


def single_char_xor(cipher):
    potential_message = []

    for value in range(256):
        message = single_char_xor_helper(cipher, value)
        score = score_english(message)
        data = {'message': message,
                'score': score,
                'key': value
                }
        potential_message.append(data)

    best = sorted(potential_message, key=lambda x: x['score'], reverse=True)[0]
    return best


def partB():
    print("\nRunning Part B")
    best_list = []
    file = open('partB.txt', 'r')

    for line in file:
        hexstring = ''.join(char for char in line if char in printable)
        cipher = bytes.fromhex(hexstring)
        best_list.append(single_char_xor(cipher))

    decoded = sorted(best_list, key=lambda x: x['score'], reverse=True)[0]
    print("Key: {}\nMessage: {}".format(decoded['key'], decoded['message'].decode('ascii')))

    file.close()


def xor(a, b):
    return bytes([x ^ y for (x, y) in zip(a, cycle(b))])


def hamDistance(a, b):
    return sum(bin(byte).count('1') for byte in xor(a, cycle(b)))


def find_keysize(b64string):
    avg_distances = []

    for keysize in range(1, len(b64string)):
        distances = []
        blocks = [b64string[i:i+keysize] for i in range(0, len(b64string), keysize)]

        while True:
            try:
                block_1 = blocks[0]
                block_2 = blocks[1]
                distance = hamDistance(block_1, block_2)

                distances.append(distance/keysize)
                del blocks[0]
                del blocks[1]

            except Exception as e:
                break

        if len(distances):
            result = {
                'key': keysize,
                'avg distance': sum(distances) / len(distances)
            }
            avg_distances.append(result)

    possible_key_lengths = sorted(avg_distances, key=lambda x: x['avg distance'])[0]
    possible_plain_text = []

    key = b''
    current_key_length = possible_key_lengths['key']
    for i in range(current_key_length):
        block = b''
        for j in range(i, len(b64string), current_key_length):
            block += bytes([b64string[j]])

        key += bytes([single_char_xor(block)['key']])
    possible_plain_text.append((xor(b64string, key), key))
    return max(possible_plain_text, key=lambda x: score_english(x[0]))


def partC():
    print("\nRunning Part C")
    file = open('partC.txt', 'r')

    b64string = b64decode(file.read())
    result, key = find_keysize(b64string)
    print("Key: {}\nMessage: {}".format(key, result.decode('ascii')))

    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    partA()
    partB()
    partC()
