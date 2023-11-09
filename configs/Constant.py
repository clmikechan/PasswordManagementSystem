class Constant:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def LENGTH(self):
        return 20

    @property
    def DATA_PATH(self):
        return 'default/data/path'

    @property
    def KEY_PATH(self):
        return 'default/key/path'

    @property
    def LINE_LENGTH(self):
        return 72

    @property
    def TAG_NAME(self):
        return 'default_data_tag'

    @property
    def ROOT_NAME(self):
        return 'default_root_tag'

constant = Constant()
