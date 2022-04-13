"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

from chardet import UniversalDetector

encode_detector = UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for item in file:
        encode_detector.feed(item)
        if encode_detector.done:
            break
    encode_detector.close()

print(encode_detector.result['encoding'])

with open('test_file.txt', 'r', encoding=encode_detector.result['encoding']) as read_file:
    for line in read_file:
        print(line)
