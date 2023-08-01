import datetime
import os
import glob
import for_mirinets
import for_mirinets_sbp

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