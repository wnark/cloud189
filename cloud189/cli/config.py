import os
import sys
from pickle import load, dump


__all__ = ['config']
KEY = 152
config_file = os.path.dirname(sys.argv[0]) + os.sep + '.config'


def encrypt(key, s):
    b = bytearray(str(s).encode("utf-8"))
    n = len(b)
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key
        c1 = b2 % 19
        c2 = b2 // 19
        c1 = c1 + 46
        c2 = c2 + 46
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("utf-8")


def decrypt(ksa, s):
    c = bytearray(str(s).encode("utf-8"))
    n = len(c)
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j + 1]
        j = j + 2
        c1 = c1 - 46
        c2 = c2 - 46
        b2 = c2 * 19 + c1
        b1 = b2 ^ ksa
        b[i] = b1
    return b.decode("utf-8")


def save_config(cf):
    with open(config_file, 'wb') as f:
        dump(cf, f)


class Config:

    def __init__(self):
        self._cookie = {}
        self._username = ""
        self._password = ""
        self._sessionKey = ""
        self._sessionSecret = ""
        self._accessToken = ""
        self._save_path = './downloads'
        self._reader_mode = False

    def _save(self):
        with open(self._config_file, 'wb') as c:
            dump(self._config, c)

    def encode(self, var):
        if isinstance(var, dict):
            for k, v in var.items():
                var[k] = encrypt(KEY, str(v))
        elif var:
            var = encrypt(KEY, str(var))
        return var

    def decode(self, var):
        try:
            if isinstance(var, dict):
                dvar = {}  # 新开内存，否则会修改原字典
                for k, v in var.items():
                    dvar[k] = decrypt(KEY, str(v))
            elif var:
                dvar = decrypt(KEY, var)
            else:
                dvar = None
        except Exception as e:
            # print(e)
            dvar = None
        return dvar

    @property
    def cookie(self):
        return self.decode(self._cookie)

    @cookie.setter
    def cookie(self, value):
        self._cookie = self.encode(value)
        save_config(self)

    @property
    def username(self):
        return self.decode(self._username)

    @username.setter
    def username(self, value):
        self._username = self.encode(value)
        save_config(self)

    @property
    def password(self):
        return self.decode(self._password)

    @password.setter
    def password(self, value):
        self._password = self.encode(value)
        save_config(self)

    @property
    def key(self):
        return self.decode(self._sessionKey)

    @key.setter
    def key(self, value):
        self._sessionKey = self.encode(value)
        save_config(self)

    @property
    def secret(self):
        return self.decode(self._sessionSecret)

    @secret.setter
    def sectet(self, value):
        self._sessionSecret = self.encode(value)
        save_config(self)

    @property
    def token(self):
        return self.decode(self._accessToken)

    @token.setter
    def token(self, value):
        self._accessToken = self.encode(value)
        save_config(self)

    def set_token(self, key, secret, token):
        '''设置全部'''
        self._sessionKey = self.encode(key)
        self._sessionSecret = self.encode(secret)
        self._accessToken = self.encode(token)
        save_config(self)

    @property
    def save_path(self):
        return self._save_path

    @save_path.setter
    def save_path(self, value):
        self._save_path = value
        save_config(self)

    @property
    def reader_mode(self):
        return self._reader_mode

    @reader_mode.setter
    def reader_mode(self, value: bool):
        self._reader_mode = value
        save_config(self)


# 全局配置对象
try:
    with open(config_file, 'rb') as c:
        config = load(c)
except:
    config = Config()
