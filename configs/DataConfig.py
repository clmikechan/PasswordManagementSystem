from configs.Constant import constant

class DataConfig:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def LENGTH(self):
        return constant.LENGTH

    @property
    def LENGTH_OF_LENGTH(self):
        return len(str(self.LENGTH))

    @property
    def PASSWORD_FIX_PATTERN(self):
        return '{:0>' + str(self.LENGTH_OF_LENGTH) + 'd}{:' + str(self.LENGTH) + '}'

    @property
    def DATA_PATH(self):
        return constant.DATA_PATH

    @property
    def KEY_PATH(self):
        return constant.KEY_PATH

    @property
    def LINE_LENGTH(self):
        return constant.LINE_LENGTH

    @property
    def TAG_NAME(self):
        return constant.TAG_NAME

    @property
    def ROOT_NAME(self):
        return constant.ROOT_NAME

data_config = DataConfig()
