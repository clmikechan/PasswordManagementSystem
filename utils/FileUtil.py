from bs4 import BeautifulSoup as bs
from base64 import b64encode, b64decode

from configs.DataConfig import data_config
from models.DataModel import DataModel

def write_data(all_data):
    data_xml = bs(f'<{data_config.ROOT_NAME}></{data_config.ROOT_NAME}>', 'xml')
    key_xml = bs(f'<{data_config.ROOT_NAME}></{data_config.ROOT_NAME}>', 'xml')
    for data in all_data:
        data_xml.find(data_config.ROOT_NAME).append(data.data_tag())
        key_xml.find(data_config.ROOT_NAME).append(data.key_tag())

    data = b64encode(str(data_xml).encode()).decode()
    with open(data_config.DATA_PATH, 'w') as data_file:
        index = 0
        while index < len(data):
            data_file.write(data[index: index + data_config.LINE_LENGTH])
            data_file.write('\n')
            index += data_config.LINE_LENGTH

    key = b64encode(str(key_xml).encode()).decode()
    with open(data_config.KEY_PATH, 'w') as key_file:
        index = 0
        while index < len(key):
            key_file.write(key[index: index + data_config.LINE_LENGTH])
            key_file.write('\n')
            index += data_config.LINE_LENGTH

def read_data():
    data_buffer = ''
    try:
        with open(data_config.DATA_PATH) as data_file:
            while (line := data_file.readline()) is not None and len(line) > 0:
                data_buffer += line
    except FileNotFoundError:
        return []

    data_reader = bs(b64decode(data_buffer.encode()).decode(), 'xml')

    key_buffer = ''
    try:
        with open(data_config.KEY_PATH) as key_file:
            while (line := key_file.readline()) is not None and len(line) > 0:
                key_buffer += line
    except FileNotFoundError:
        return []

    key_reader = bs(b64decode(key_buffer.encode()).decode(), 'xml')

    d = {}
    for data in data_reader.find_all(data_config.TAG_NAME):
        d[data.find('name').string] = [data]

    for data in key_reader.find_all(data_config.TAG_NAME):
        d[data.find('name').string].append(data)

    all_data = []
    for data in d:
        all_data.append(DataModel.by_tag(d[data][0], d[data][1]))

    return all_data
