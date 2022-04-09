"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b''.
"""

word_1 = 'attribute'
word_2 = 'класс'
word_3 = 'функция'
word_4 = 'type'

word_list = [word_1, word_2, word_3, word_4]

for item in word_list:
    try:
        print(bytes(item, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{item}" невозможно записать в виде байтовой строки')
