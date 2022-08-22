import datetime
import os
import glob

directory = r"Z:\_СПЛИТ_not_delete\02_Инженерно-геофизическая служба\02_Проекты\02_2021_ВС море\07_Отчетные_материалы\06_Фонды\02.3_HDD_В-С-1 ЛУ_испр\ES LU\02_nav\01_VHR"
firstChar = 8  # первый символ названия профиля в названии файла (начиная с 0)
lastChar = 15  # последний символ названия профиля в названии файла(не включительно)
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
    """

    if recursive_:
        allTextFiles = []
        for rootDir, dirs, files in os.walk(path):
            allTextFiles.extend(list(map(lambda x: rootDir + '\\' + x, filter(lambda x: x.endswith('.txt'), files))))
            print(allTextFiles)
    else:
        allTextFiles = glob.glob(path + r"\**\*.txt")
        print(allTextFiles)
    for file in allTextFiles:
        *pathFile, fileName = file.split('\\')
        pathFile = '\\'.join(pathFile)
        with open(file, 'r+') as f:
            firstLine = 'NAME' + '\t' + 'DATE' + '\t' + f.readline()[5:]  # Названия столбцов
            lines = f.readlines()
            for i in range(len(lines)):
                subLines = lines[i].split('\t')
                year, day = subLines[yearColumn], subLines[dayColumn]
                date = datetime.datetime.strptime(year + day, '%Y%j').strftime('%d.%m.%Y')
                lines[i] = fileName[firstCh:lastCh] + '\t' + date + '\t' + lines[i][5:]

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
