import codecs
import base64

def ConvertToHex(message):
    return codecs.encode(str.encode(message), "hex").decode("ascii")

def ConvertFromHex(hexcode):
    return codecs.decode(hexcode, "hex").decode("ascii")

def ConvertTo64(message):
    return base64.encodebytes(str.encode(message)).decode("ascii")

def ConvertFrom64(code):
    return base64.decodebytes(code).decode("ascii")