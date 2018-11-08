import sqlite3

from time import sleep

def sumAndMed(dbName: str):
    # connect = sqlite3.connect(dbName)

    # res = connect.execute('''Select
    #                 (Case
    #                 When b.total %2 = 1 then (Select float from 
    #                 (SELECT float, ROW_NUMBER() OVER(ORDER BY float) AS num FROM file_inf) as a
    #                 where num = round(b.total/2))
    #                 When b.total %2 = 0 then (Select avg(float) from 
    #                 (SELECT float, ROW_NUMBER() OVER(ORDER BY float) AS num FROM file_inf) as a
    #                 where num = round(b.total/2) or num = round(b.total/2) + 1 ) 
    #                 End) as mediana
    #                 From (Select count(*) as total from file_inf) as b	''')
    # connect.close()
    # return res
    pass

def importToDB(dbName: str, win, fileName: str):
    connect = sqlite3.connect(dbName)
    cursor = connect.cursor()

    try:
        cursor.execute('''CREATE TABLE file_inf
                    (date TEXT, kirilic TEXT, latinic TEXT, int INTEGER, float REAL) ''')
    except sqlite3.OperationalError as e:
        print(e)

    connect.commit()

    f = open(fileName)

    strings = f.readlines()

    ls = []

    for string in strings:
        item = string.split('||')[:-1]
        item[-1] = float(item[-1].replace(',','.'))
        item[-2] = int(item[-2])
        ls.append(item)
    win.statusbarMessage('start')
    print('strt')
    #connect.executemany("INSERT INTO file_inf VALUES (?,?,?,?,?)", ls)
    count = 0
    for item in ls:
        connect.execute("INSERT INTO file_inf VALUES (?,?,?,?,?)", item)
        count += 1
        if count == 100:
            win.statusbarMessage("inserted %d lines of %d to %s" % (ls.index(item),len(ls),fileName))
            count = 0
        
    connect.commit()
    win.statusbarMessage("import complete from %s" % (fileName))
    print("end")
    connect.close()