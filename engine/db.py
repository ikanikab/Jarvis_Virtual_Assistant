import sqlite3

conn = sqlite3.connect("jarvis.db")

cursor = conn.cursor()

query = "create table if not exists sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# for deletion
# query = "delete from sys_command where id=3"

# insertion
query = "insert into sys_command values (3, 'powerpoint' ,'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')"
cursor.execute(query)
conn.commit()

query = "create table if not exists web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# query = "insert into web_command values (null, 'spotify' ,'https://open.spotify.com/')"
# cursor.execute(query)
# conn.commit()