import random
import math
import re
from Crypto.Cipher import AES
import base64


def gas(data, key0, iv0):
    key = re.sub(r'/(^\s+)|(\s+$)/g', '', key0).encode('utf-8')
    iv = iv0.encode('utf-8')

    BS = AES.block_size
    def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    x = len(data) % 8
    if x != 0:
        data = data + '\0' * (8 - x)

    encrypted = AES.new(key, AES.MODE_CBC, iv)
    d = encrypted.encrypt(pad(data))
    return base64.standard_b64encode(d).decode("utf-8")


def rds(length):
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    chars_len = len(chars)
    retStr = ''
    for i in range(length):
        retStr += chars[math.floor(random.random() * chars_len)]
    return retStr


def encryptAES(data, p1):
    if not p1:
        return data
    return gas(rds(64)+data, p1, rds(16))
