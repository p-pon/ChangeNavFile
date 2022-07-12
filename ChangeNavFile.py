import datetime
import os
import glob


directory = r"C:\Users\pavel.ponimaskin\PycharmProjects\for sasha\files\СУВР"
firstChar = 4  # первый символ названия профиля в названии файла
lastChar = 11  # последний символ названия профиля в названии файла
recursive = True  # искать .txt файлы во всех подкаталогах пути?
ChangeFile = False  # заменять корневой файл?
yearColumn = 0  # № колонки "Год" в файле
dayColumn = 1  # № колонки "Юлианский день" в файле


def add_columns(path, firstCh, lastCh, recursive_=True, ChangeFile_=False):
    """
    Функция предназначена для изменения текстовых файлов с навигационными данными.
    Добавляет колонки:
     - NAME (из имени файла)
     - DATE формата "dd.mm.YYYY" (из колонок yearColumn, dayColumn формата "YYYY jjj")

    :param path: директория с файлами для изменения.
    :param firstCh: первый символ названия профиля в названии файла.
    :param lastCh: последний символ названия профиля в названии файла.
    :param recursive_: искать .txt файлы во всех подкаталогах пути?
    :param ChangeFile_: заменять корневой файл или создавать папку changed с измененными файлами.
    """

    if recursive_:
        allTextFiles = []
        for rootDir, dirs, files in os.walk(path):
            allTextFiles.extend(list(map(lambda x: rootDir + '\\' + x, filter(lambda x: x.endswith('.txt'), files))))
    else:
        allTextFiles = glob.glob(path + r"\**\*.txt")
    for file in allTextFiles:
        *pathFile, fileName = file.split('\\')
        pathFile = '\\'.join(pathFile)
        with open(file, 'r+') as f:
            firstLine = 'NAME' + '\t' + 'DATE' + '\t' + f.readline()  # Названия столбцов
            lines = f.readlines()
            for i in range(len(lines)):
                subLines = lines[i].split('\t')
                year, day = subLines[yearColumn], subLines[dayColumn]
                date = datetime.datetime.strptime(year+day, '%Y%j').strftime('%d.%m.%Y')
                lines[i] = fileName[firstCh:lastCh + 1] + '\t' + date + '\t' + lines[i]

            if ChangeFile_:
                f.seek(0)
                print(firstLine, *lines, sep='', file=f)
            else:
                try:
                    with open(pathFile + '\\changed\\' + fileName, 'w') as fn:
                        print(firstLine, *lines, sep='', file=fn)
                except FileNotFoundError:
                    os.mkdir(pathFile + '\\changed')
                    with open(pathFile + '\\changed\\' + fileName, 'w') as fn:
                        print(firstLine, *lines, sep='', file=fn)


add_columns(directory, firstChar, lastChar, recursive, ChangeFile)
