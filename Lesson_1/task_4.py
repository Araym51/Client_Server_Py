"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

word_1 = 'разработка'
word_2 = 'администрирование'
word_3 = 'protocol'
word_4 = 'standard'

word_list = [word_1, word_2, word_3, word_4]

byte_words = []
for i in word_list:
    i = i.encode('utf-8')
    byte_words.append(i)

print(byte_words)
print('-----')

decoded_words = []
for j in byte_words:
    j = j.decode('utf-8')
    decoded_words.append(j)

print(decoded_words)
