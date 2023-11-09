from bs4 import BeautifulSoup as bs
from base64 import b64encode, b64decode
#from random import randint
from secrets import token_bytes

from configs.DataConfig import data_config
class DataModel:
    '''
    基本欄位: 
    key: 用來加密資訊用之 key. 有幾個欄位需要加密就有幾個 key
    kind: 類別
    subkind: 子類別
    *password*: 密碼
    *id*: 帳號(登入系統用之帳號, 非銀行帳號)
    name: 銀行名稱
    除此之外都統稱為 other(個別銀行有所不同)

    目前只有帳號密碼有加密
    '''
    def __init__(self, kind, subkind, name, id_, password, id_key=None, password_key=None, **kwargs):
        self.id_key = id_key

        self.password_key = password_key

        self.id = id_

        self.password = password

        self.__name = name
        self.__kind = kind
        self.__subkind = subkind
        self.__other = kwargs


    @staticmethod
    def encrypt(key, data):
        fix = data_config.PASSWORD_FIX_PATTERN.format(len(data), data)
        key = b64decode(key.encode())
        return b64encode(bytes([a ^ b for a, b in zip(list(fix.encode()), list(key))])).decode()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def kind(self):
        return self.__kind

    @kind.setter
    def kind(self, kind):
        self.__kind = kind

    @property
    def subkind(self):
        return self.__subkind

    @subkind.setter
    def subkind(self, subkind):
        self.__subkind = subkind

    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, id_):
        self.__id = DataModel.encrypt(self.id_key, id_)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = DataModel.encrypt(self.password_key, password)

    @property
    def id_key(self):
        return self.__id_key

    @id_key.setter
    def id_key(self, id_key=None):
        if id_key is None:
            #id_key = bytes([randint(0, 255) for _ in range(data_config.LENGTH + data_config.LENGTH_OF_LENGTH)])
            id_key = token_bytes(data_config.LENGTH + data_config.LENGTH_OF_LENGTH)
        else:
            id_key = id_key
        self.__id_key = b64encode(id_key).decode()

    @property
    def password_key(self):
        return self.__password_key

    @password_key.setter
    def password_key(self, password_key=None):
        if password_key is None:
            #password_key = bytes([randint(0, 255) for _ in range(data_config.LENGTH + data_config.LENGTH_OF_LENGTH)])
            password_key = token_bytes(data_config.LENGTH + data_config.LENGTH_OF_LENGTH)
        else:
            password_key = password_key
        self.__password_key = b64encode(password_key).decode()

    def refresh_key(self):
        id_ = self.get_id
        password = self.get_password

        self.id_key = None
        self.password_key = None

        self.id = id_
        self.password = password

    def get_attr_list(self):
        return self.__other.keys()

    def get_attr(self, key, default=None):
        return self.__other.get(key, default)

    def set_attr(self, key, value):
        self.__other[key] = value

    def remove_attr(self, key):
        if key in self.__other:
            del self.__other[key]

    @staticmethod
    def decrypt(key, data):
        password = bytes([a ^ b for a, b in zip(list(b64decode(data.encode())), list(b64decode(key.encode())))]).decode()
        length = int(password[0: data_config.LENGTH_OF_LENGTH])
        return password[data_config.LENGTH_OF_LENGTH: data_config.LENGTH_OF_LENGTH + length]

    @property
    def get_id(self):
        return DataModel.decrypt(self.id_key, self.id)

    @property
    def get_password(self):
        return DataModel.decrypt(self.password_key, self.password)

    @staticmethod
    def append_tag(soup, key, value):
        tag = bs().new_tag(key)
        tag.string = value
        soup.append(tag)

    def key_tag(self):
        data = bs().new_tag(data_config.TAG_NAME)
        DataModel.append_tag(data, 'kind', self.kind)
        DataModel.append_tag(data, 'subkind', self.subkind)
        DataModel.append_tag(data, 'name', self.name)
        DataModel.append_tag(data, 'id_key', self.id_key)
        DataModel.append_tag(data, 'password_key', self.password_key)
        return data

    def data_tag(self):
        data = bs().new_tag(data_config.TAG_NAME)
        DataModel.append_tag(data, 'kind', self.kind)
        DataModel.append_tag(data, 'subkind', self.subkind)
        DataModel.append_tag(data, 'name', self.name)
        DataModel.append_tag(data, 'id', self.id)
        DataModel.append_tag(data, 'password', self.password)
        for key in self.get_attr_list():
            DataModel.append_tag(data, key, self.get_attr(key))

        return data

    @staticmethod
    def by_tag(data, key):
        id_ = DataModel.decrypt(key.id_key.string, data.id.string)
        password = DataModel.decrypt(key.password_key.string, data.password.string)
        d = dict([(x.name, x.text) for x in data.find_all() if x.name not in ('kind', 'subkind', 'name', 'id', 'password')])
        return DataModel(data.kind.string, data.subkind.string, data.find('name').string, id_, password, b64decode(key.id_key.string), b64decode(key.password_key.string), **d)
