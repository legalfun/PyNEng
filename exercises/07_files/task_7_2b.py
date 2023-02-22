#!/usr/bin/env python
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]
from sys import argv
in_file, out_file = argv[1], argv[2]
#out_file.close()
with open(in_file) as i_f, open(out_file, 'w') as o_f:
    for line in i_f:
        if not set(ignore) & set(line.strip()) and not line.startswith('!'):
            o_f.write(line)
#out_file.close()
