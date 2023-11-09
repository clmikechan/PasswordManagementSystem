from secrets import choice, randbelow
from random import randint
import unittest

ERR_MSG1 = 'groups should disjoint and not have duplicate char'
ERR_MSG2 = 'Number of group must less than or equal to {}'

NUMBER_GROUP = r'0123456789'
UPPER_LETTER_GROUP = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_LETTER_GROUP = r'abcdefghijklmnopqrstuvwxyz'
PUNCTUATION_GROUP = r'`~!@#$%^*()_-+=|\]}[{;:,./?'
STANDARD_GROUPS = [NUMBER_GROUP, UPPER_LETTER_GROUP, LOWER_LETTER_GROUP, PUNCTUATION_GROUP]

def valid_groups(*groups):
    concate = ''.join(groups)
    return len(set(concate)) == len(concate)

def generate_password(min_: int, max_: int, *groups):
    number_of_group = len(groups)
    if not valid_groups(*groups):
        raise ValueError(ERR_MSG1)

    if min_ < number_of_group:
        raise ValueError(ERR_MSG2.format(min_))

    unused = list(range(number_of_group))
    size = randint(min_, max_)
    builder = []
    for i in range(size):
        unused_count = len(unused)
        if unused_count > 0 and i + len(unused) == size:
            group_index = choice(unused)
            unused.pop(unused.index(group_index))
            builder.insert(i + 1, choice(groups[group_index]))
        else:
            group_index = randbelow(number_of_group)
            builder.insert(i + 1, choice(groups[group_index]))

    return ''.join(builder)



class GeneratePasswordTest(unittest.TestCase):
    def testGenerate(self):
        min_ = 6
        max_ = 20
        groups = STANDARD_GROUPS
        password = generate_password(min_, max_, *groups)
        self.assertTrue(min_ <= len(password) <= max_)
        for group in groups:
            self.assertTrue(
                set(password).intersection(set(group))
            )

        print(password)

    def testDuplicateGroup(self):
        min_ = 6
        max_ = 20
        groups = [NUMBER_GROUP, r'A' + UPPER_LETTER_GROUP, LOWER_LETTER_GROUP, PUNCTUATION_GROUP]
        with self.assertRaises(ValueError) as e:
            generate_password(2, 12, *groups)

        self.assertEqual(str(e.exception), ERR_MSG1)

    def testJointGroup(self):
        min_ = 6
        max_ = 20
        groups = [NUMBER_GROUP + r'A', UPPER_LETTER_GROUP, LOWER_LETTER_GROUP, PUNCTUATION_GROUP]
        with self.assertRaises(ValueError) as e:
            generate_password(2, 12, *groups)

        self.assertEqual(str(e.exception), ERR_MSG1)

    def testTooManyGroup(self):
        min_ = 2
        max_ = 12
        groups = STANDARD_GROUPS
        with self.assertRaises(ValueError) as e:
            generate_password(2, 12, *groups)

        self.assertEqual(str(e.exception), ERR_MSG2.format(min_))

if __name__ == '__main__':
    unittest.main()
