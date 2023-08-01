import datetime
import glob
import os

directory = r"C:\Users\pavel.ponimaskin\PycharmProjects\for sasha\01_UTM"
path_navFiles = r'C:\Users\pavel.ponimaskin\PycharmProjects\for sasha\nav'
firstChar = 8  # первый символ названия профиля в названии файла
lastChar = 17  # последний символ названия профиля в названии файла
recursive = True  # искать .txt файлы во всех подкаталогах пути?
ChangeFile = False  # заменять корневой файл?
yearColumn = 0  # № колонки "Год" в файле
dayColumn = 1  # № колонки "Юлианский день" в файле


def add_columns(path, path_nF, firstCh, lastCh, recursive_=True, ChangeFile_=False):
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
        allNavFiles = []
        for rootDir, dirs, files in os.walk(path):
            allTextFiles.extend(list(map(lambda x: rootDir + '\\' + x, filter(lambda x: x.endswith('.txt'), files))))
        for rootDir, dirs, files in os.walk(path_nF):
            allNavFiles.extend(list(map(lambda x: rootDir + '\\' + x, filter(lambda x: x.endswith('.txt'), files))))
    else:
        allTextFiles = glob.glob(path + r"\**\*.txt")
        allNavFiles = glob.glob(path_nF + r"\**\*.txt")

    for file in allTextFiles:
        *pathFile, fileName = file.split('\\')
        pathFile = '\\'.join(pathFile)
        with open(file, 'r+') as f:
            firstLine = 'NAME' + '\t' + 'DATE' + '\t' + f.readline()  # Названия столбцов
            lines = f.readlines()
            with open(path_nF + '\\' + fileName) as f_nav:
                lines_nav = f_nav.readlines()
            for i in range(len(lines)):
                subLines = lines[i].split('\t')
                subline_nav = lines_nav[i].split('; ')
                year, day = subLines[yearColumn], subLines[dayColumn]
                subLines[6], subLines[7] = subline_nav[1], subline_nav[2]
                date = datetime.datetime.strptime(year+day, '%Y%j').strftime('%d.%m.%Y')
                lines[i] = fileName[firstCh:lastCh + 1] + '\t' + date + '\t' + '\t'.join(subLines) + '\n'
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


add_columns(directory, path_navFiles, firstChar, lastChar, recursive, ChangeFile)
