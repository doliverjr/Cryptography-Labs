from datetime import datetime
import base64, datetime, hashlib, os
import binascii

w = 32
n = 624
m = 397
r = 31
a = 0x9908B0DF
u = 11
d = 0xFFFFFFFF
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
f = 1812433253


class MT19937:
    def __init__(self, seed):
        self.MT = [0] * n
        self.index = n+1
        self.lower_mask = (1 << r) - 1
        self.upper_mask = ~self.lower_mask & ((1 << w) - 1)
        self.seed = seed
        self.seed_mt(seed)

    def seed_mt(self, seed):
        self.index = n
        self.MT[0] = seed
        for i in range(1, n):
            self.MT[i] = (f * (self.MT[i-1] ^ (self.MT[i-1] >> (w-2))) + i) & ((1 << w) - 1)

    def extract_number(self):
        if self.index >= n:
            if self.index > n:
                print("Error: Generator was never seeded")

            self.twist()

        y = self.MT[self.index]
        y1 = y ^ ((y >> u) & d)
        y2 = y1 ^ ((y1 << s) & b)
        y3 = y2 ^ ((y2 << t) & c)
        z = y3 ^ (y3 >> l)

        self.index += 1
        return z & ((1 << w) - 1)

    def twist(self):
        for i in range(n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA ^= a
            self.MT[i] ^= xA

        self.index = 0


    def unmix(self):
        tokens = []
        for i in range(78):
            z = self.extract_number()
            y3 = z ^ (z >> l)
            y2 = y3 ^ ((y3 << t) & c)
            y1 = y2
            mask = 0x7f
            for i in range(4):
                temp = b & (mask << (7 * (i + 1)))
                y1 = y1 ^ ((y1 << s) & temp)

            y = y1
            for i in range(3):
                y = y ^ (y >> u)

            tokens.append(y)

        return tokens


def unmix(mixNum):
    z = mixNum
    y3 = z ^ (z >> l)
    y2 = y3 ^ ((y3 << t) & c)
    y1 = y2
    mask = 0x7f
    for i in range(4):
        temp = b & (mask << (7 * (i + 1)))
        y1 = y1 ^ ((y1 << s) & temp)

    y = y1
    for i in range(3):
        y = y ^ (y >> u)

    return y


#creates a token based on a given generator
def get_token(MT):
    token = str(MT.extract_number())
    for i in range(7):
        token += ":" + str(MT.extract_number())
    return base64.b64encode(bytes(str(token), encoding='ascii'))


def decodeTokens(tokens):
    out = []
    for i in tokens:
        i = base64.b64decode(i).decode("utf-8")
        for j in i.split(':'):
            out.append(unmix(int(j)))
    return out

#creating a clone of a MT based on the known MT.MT
def createClone(values):
    clone = MT19937(0);
    clone.MT = values
    clone.index = n
    return clone

def writeTokens(tokens):
    f = open("tokens.txt", "w+")
    out = ""
    for i in tokens:
        out = i.decode("utf-8")
        out += "\n"
        f.write(out)

#read tokens from a file, seperate, and unmix them
def readTokens(filename):
    with open(filename, "r") as f:
        temp = f.readlines()

    for i in range(len(temp)):
        temp[i] = temp[i].strip()

    tokens = decodeTokens(temp)
    return tokens


if __name__ == '__main__':
    wtoken = []
    tokens = []
    seed = int.from_bytes(os.urandom(4), "big")
    MT = MT19937(seed)

    #generate a random token file
    for i in range(78):
        wtoken.append(get_token(MT))
    writeTokens(wtoken)
    #read file and clone the PRG
    tokens = readTokens("tokens.txt")
    clone = createClone(tokens)

    #get one more token of each to see if they match
    fake = get_token(clone)
    real = get_token(MT)
    print(f"Cloned Token:{fake}\nReal Token:{real}\nMatch:{real==fake}")
