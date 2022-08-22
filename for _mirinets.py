import datetime
import os
import glob

directory = r"Z:\_СПЛИТ_not_delete\02_Инженерно-геофизическая служба\02_Проекты\02_2021_ВС море\07_Отчетные_материалы\06_Фонды\02.3_HDD_В-С-1 ЛУ_испр\ES LU\02_nav\02_UHR"
firstChar = 8  # первый символ названия профиля в названии файла (начиная с 0)
lastChar = 15  # последний символ названия профиля в названии файла(не включительно)
recursive = True  # искать .txt файлы во всех подкаталогах пути?
ChangeFile = False  # заменять корневой файл?
yearColumn = 0  # № колонки "Год" в файле
dayColumn = 1  # № колонки "Юлианский день" в файле
EBCDIC = '''H001 SURVEY AREA: EAST SIBERIAN SEA, EAST-SIBERIAN-1 LU (ES_IGI)                                 
H002 VESSEL: R/V KERN                 
H003 CLIENT: ROSNEFT/ARCTIC RESEARCH CENTER
H004 CONTRACTOR: LLC SPLIT
H005 SURVEY: ULTRA HIGH-RESOLUTION SEISMIC                                                                                                                                                                                                                                  
H006 NAVIGATION PARAMETERS SURVEY:  
H007 MAP PROJECTION: UNIVERSAL TRANSVERSE MERCATOR (UTM) 
H008 ZONE: 58N; DATUM: WGS-84; CENTRAL MERIDIAN: 165
H009 ORIGIN LATITUDE: 0; FALSE EASTING: 500000
H010 FALSE NORTHING: 0; SCALE FACTOR: 0.9996; COORDINATE UNITS: m 
H011 NAVIGATION PARAMETERS PROCESSED: 
H012 MAP PROJECTION: GAUSS KRUEGER; ZONE: 28; DATUM: GSK-2011; CENTRAL MERIDIAN: 165
H013 ORIGIN LATITUDE: 0; FALSE EASTING: 25500000
H014 FALSE NORTHING: 0; SCALE FACTOR: 1; COORDINATE UNITS: m   '''
EBCDIC = ''.join(map(lambda x: x.strip() + '\n', EBCDIC.split('\n')))


def add_columns(path, firstCh, lastCh, recursive_=True, ChangeFile_=False):
    """
    Функция предназначена для изменения текстовых файлов с навигационными данными.
    Добавляет колонки:
     - NAME (из имени файла)
     - DATE формата "dd.mm.YYYY" (из колонок yearColumn, dayColumn формата "YYYY jjj")
     формат:
     name->dd.mm.yyyy->hh->mm->ss->ms->SP->X->Y
     файлы UHR, VHR
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
            firstLine = '\t'.join(['NAME', 'DATE', *true_first_line[2:6], 'Shot_Point', *true_first_line[10:]])
            # print(firstLine)

            lines = f.readlines()
            for i in range(len(lines)):
                subLines = lines[i].split('\t')
                year, day = '2021', subLines[dayColumn]
                try:
                    date = datetime.datetime.strptime(year + day, '%Y%j').strftime('%d.%m.%Y')
                except ValueError:
                    print(i, subLines, file)
                    del lines[i]
                    continue
                # lines[i] = fileName[firstCh:lastCh] + '\t' + date + '\t' + lines[i][5:]
                lines[i] = '\t'.join([fileName[firstCh:lastCh], date, *subLines[2:6], subLines[0], *subLines[10:]])
                # print(lines[i])
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
