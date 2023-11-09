import re

from models.DataModel import DataModel
from utils.FileUtil import write_data, read_data
from utils.PasswordUtil import NUMBER_GROUP, UPPER_LETTER_GROUP, LOWER_LETTER_GROUP, PUNCTUATION_GROUP, STANDARD_GROUPS, generate_password

PATTERN = re.compile('^[0-9]+$')

def print_data(row):
    print(f'kind = {row.kind}')
    print(f'subkind = {row.subkind}')
    print(f'name = {row.name}')
    print(f'id = {row.get_id}')
    print(f'password = {row.get_password}')
    for attr in row.get_attr_list():
        print(f'{attr} = {row.get_attr(attr)}')

def get_row_index(all_data , arg):
    if PATTERN.match(arg):
        return int(arg)
    else:
        for index, row in enumerate(all_data):
            if row.name == arg:
                return index

def get_data(arg):
    all_data = read_data()
    print_data(all_data[get_row_index(all_data , arg)])

def put_data(arg):
    all_data = read_data()
    kind = arg[0]
    subkind = arg[1]
    name = arg[2]
    id_ = arg[3]
    for i, x in enumerate(all_data):
        if kind == x.kind and subkind == x.subkind and name == x.name:
            raise ValueError('Duplicate Data')

    password = arg[4]
    i = 5
    data = {}

    while i + 1 < len(arg):
        data[arg[i]] = arg[i + 1]
        i += 2

    newData = DataModel(name, id_, password, **data)

    all_data.append(newData)

    write_data(all_data)

def update_data(arg):
    all_data = read_data()
    row = all_data[get_row_index(all_data , arg[0])]

    data = {}
    i = 1
    while i + 1 < len(arg):
        if arg[i] not in ('name', 'id'):
            data[arg[i]] = arg[i + 1]

        i += 2

    if 'password' in data:
        row.password = data['password']
        del data['password']

    for k, v in data.items():
        row.set_attr(k, v)

    write_data(all_data)

def remove_param(arg):
    all_data = read_data()
    row = all_data[get_row_index(all_data , arg[0])]

    for param in arg[1:]:
        if param not in ('kind', 'subkind', 'name', 'id', 'password'):
            row.remove_attr(param)

    write_data(all_data)

def refresh_key(arg):
    all_data = read_data()
    row_index = get_row_index(all_data , arg)
    row = all_data[row_index]

    row.refresh_key()

    write_data(all_data)

def do_generate_password(arg):
    min_ = int(arg[0])
    max_ = int(arg[1])
    if 'STANDARD_GROUPS' == arg[2] or arg[2] == '0':
        return generate_password(min_, max_, *STANDARD_GROUPS)

    groups = []
    for x in arg[2:]:
        if x == 'NUMBER_GROUP':
            groups.append(NUMBER_GROUP)
        elif x == '1':
            groups.append(NUMBER_GROUP)
        elif x == 'UPPER_LETTER_GROUP':
            groups.append(UPPER_LETTER_GROUP)
        elif x == '2':
            groups.append(UPPER_LETTER_GROUP)
        elif x == 'LOWER_LETTER_GROUP':
            groups.append(LOWER_LETTER_GROUP)
        elif x == '3':
            groups.append(LOWER_LETTER_GROUP)
        elif x == 'PUNCTUATION_GROUP':
            groups.append(PUNCTUATION_GROUP)
        elif x == '4':
            groups.append(PUNCTUATION_GROUP)
        else:
            groups.append(x)

    return generate_password(min_, max_, *groups)

if __name__ == '__main__':
    from sys import argv
    if argv[1] == '0':
        get_data(argv[2])
    elif argv[1] == '1':
        put_data(argv[2:])
    elif argv[1] == '2':
        update_data(argv[2:])
    elif argv[1] == '3':
        remove_param(argv[2:])
    elif argv[1] == '4':
        refresh_key(argv[2])
    elif argv[1] == '5':
        print(do_generate_password(argv[2:]))