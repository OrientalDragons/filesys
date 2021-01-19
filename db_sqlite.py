import sqlite3

database= './x/db_sqlite.db'
con = sqlite3.connect(database)
# sql = '''CREATE TABLE IF NOT EXISTS filelist(status INTEGER,name TEXT PRIMARY KEY)'''
# cur = con.cursor()
# cur.execute(sql)
# data = (1,'test.xlsx')
# cur.execute("INSERT INTO filelist values(?,?)", data)
# con.commit()
# con.close()

filename = 'test.xlsxx'
sql = '''SELECT status FROM filelist WHERE name = ? '''
cur = con.cursor()
cur.execute("UPDATE filelist SET status = 2 WHERE name = ?", (filename,))
con.commit()
cur.execute(sql, (filename,))
print(cur.fetchone()==None)
con.commit()
