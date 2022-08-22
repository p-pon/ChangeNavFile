import datetime
import os
import glob

directory = r"Z:\_СПЛИТ_not_delete\02_Инженерно-геофизическая служба\02_Проекты\02_2021_ВС море\07_Отчетные_материалы\06_Фонды\03.3_HDD_A-Н ЛУ_испр\AN LU\02_nav\04_SSS"
firstChar = 8  # первый символ названия профиля в названии файла (начиная с 0)
lastChar = 15  # последний символ названия профиля в названии файла(не включительно)
recursive = True  # искать .txt файлы во всех подкаталогах пути?
ChangeFile = False  # заменять корневой файл?
yearColumn = 0  # № колонки "Год" в файле
dayColumn = 1  # № колонки "Юлианский день" в файле
EBCDIC = '''H001 SURVEY AREA: LAPTEV SEA, ANISINSKO-NOVOSIBIRSKIY LU (AN_IGI)                                 
H002 VESSEL: R/V KERN                 
H003 CLIENT: ROSNEFT/ARCTIC RESEARCH CENTER
H004 CONTRACTOR: LLC SPLIT
H005 SURVEY: SIDE-SCAN SONAR                                                                                                                                                                                                                                 
H006 NAVIGATION PARAMETERS SURVEY:  
H007 MAP PROJECTION: LAMBERT CONFORMAL CONIC; DATUM:  WGS-84 
H008 FIRST STANDART PARALLEL: 77.76; SECOND STANDART PARALLEL: 75.96
H009 CENTRAL MERIDIAN: 133.6; ORIGIN LATITUDE: 0; FALSE NORTHING: 0
H010 FALSE EASTING: 1000000; COORDINATE UNITS: m 
H011 NAVIGATION PARAMETERS PROCESSED: 
H012 MAP PROJECTION: GAUSS KRUEGER; ZONE: 25; DATUM: GSK-2011; CENTRAL MERIDIAN: 147
H013 ORIGIN LATITUDE: 0; FALSE EASTING: 25500000
H014 FALSE NORTHING: 0; SCALE FACTOR: 1; COORDINATE UNITS: m  '''
EBCDIC = ''.join(map(lambda x: x.strip() + '\n', EBCDIC.split('\n')))


def add_columns(path, firstCh, lastCh, recursive_=True, ChangeFile_=False):
    """
    Функция предназначена для изменения текстовых файлов с навигационными данными.
    Добавляет колонки:
     - NAME (из имени файла)
     формат:
     name->dd.mm.yyyy->hh->mm->ss->ms->SP->X->Y
     файлы SBP, SSS
    """

    if recursive_:
        allTextFiles = []
        for rootDir, dirs, files in os.walk(path):
            allTextFiles.extend(list(map(lambda x: rootDir + '\\' + x, filter(lambda x: x.endswith('.txt'), files))))
            # print(allTextFiles)
    else:
        allTextFiles = glob.glob(path + r"\**\*.txt")
        print(allTextFiles)
    for file in allTextFiles:
        *pathFile, fileName = file.split('\\')
        pathFile = '\\'.join(pathFile)
        with open(file, 'r+') as f:
            true_first_line = f.readline().split('\t')  # Названия столбцов
            firstLine = '\t'.join(
                ['NAME', 'DATE', 'HOUR', 'MINUTE', 'SECOND', 'MSEC', 'Shot_Point', 'SBP_X', 'SBP_Y']) + '\n'
            # print(firstLine)

            lines = f.readlines()
            broken_counter = 0

            for i in range(len(lines)):

                subLines = lines[i].split('\t')

                try:
                    H, M, S = subLines[2].split(':')
                    S, MS = S.split('.')
                    lines[i] = '\t'.join(
                        [fileName[firstCh:lastCh], subLines[1], H, M, S, MS, subLines[0], *subLines[3:]])
                except IndexError:
                    broken_counter += 1
            if broken_counter:
                print(file, broken_counter)
            if ChangeFile_:
                f.seek(0)
                print(firstLine, *lines, sep='', file=f)
            else:
                try:
                    with open(pathFile + '\\changed\\' + fileName, 'w') as fn:
                        print(EBCDIC, firstLine, *lines, sep='', file=fn)
                except FileNotFoundError:
                    os.mkdir(pathFile + '\\changed')
                    with open(pathFile + '\\changed\\' + fileName, 'w') as fn:
                        print(EBCDIC, firstLine, *lines, sep='', file=fn)


add_columns(directory, firstChar, lastChar, recursive, ChangeFile)
