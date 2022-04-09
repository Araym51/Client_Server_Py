"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

"""

import subprocess
import chardet

command = ['ping', 'youtube.com']
ping_youtube = subprocess.Popen(command, stdout=subprocess.PIPE)
for line in ping_youtube.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))


"""
результат:
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}


{'encoding': 'IBM866', 'confidence': 0.9308723921959009, 'language': 'Russian'}
Обмен пакетами с youtube.com [173.194.222.136] с 32 байтами данных:

{'encoding': 'IBM866', 'confidence': 0.9637267119204622, 'language': 'Russian'}
Ответ от 173.194.222.136: число байт=32 время=57мс TTL=102

{'encoding': 'IBM866', 'confidence': 0.9637267119204622, 'language': 'Russian'}
Ответ от 173.194.222.136: число байт=32 время=65мс TTL=102

{'encoding': 'IBM866', 'confidence': 0.9637267119204622, 'language': 'Russian'}
Ответ от 173.194.222.136: число байт=32 время=69мс TTL=102

{'encoding': 'IBM866', 'confidence': 0.9637267119204622, 'language': 'Russian'}
Ответ от 173.194.222.136: число байт=32 время=61мс TTL=102

{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}


{'encoding': 'IBM866', 'confidence': 0.99, 'language': 'Russian'}
Статистика Ping для 173.194.222.136:

{'encoding': 'IBM866', 'confidence': 0.9533417258006296, 'language': 'Russian'}
    Пакетов: отправлено = 4, получено = 4, потеряно = 0

{'encoding': 'IBM866', 'confidence': 0.99, 'language': 'Russian'}
    (0% потерь)

{'encoding': 'IBM866', 'confidence': 0.99, 'language': 'Russian'}
Приблизительное время приема-передачи в мс:

{'encoding': 'IBM866', 'confidence': 0.9955163083206161, 'language': 'Russian'}
    Минимальное = 57мсек, Максимальное = 69 мсек, Среднее = 63 мсек
"""