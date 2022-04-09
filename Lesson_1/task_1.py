"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить
в строковом формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление
в набор кодовых точек Unicode и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - строковый формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""
word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'

words = [word_1, word_2, word_3]

for i in words:
    print(type(i))
    print(i)

print('-----')

word_4 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
word_5 = '\u0441\u043e\u043a\u0435\u0442'
word_6 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

uni_words = [word_4, word_5, word_6]

for j in uni_words:
    print(type(j))
    print(j)

