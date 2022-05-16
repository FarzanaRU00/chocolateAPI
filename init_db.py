import sqlite3

connection = sqlite3.connect('chocolates.db')
# importing sqlite3 and connecting it to the database we created

with open('chocolates.sql') as f:
    connection.executescript(f.read())
# opening the sql file we made and execute multiple SQL statements with executescript() 

cur = connection.cursor()
# creating a cursor object = processes rows in a db

cur.execute("INSERT INTO chocolates (name, country) VALUES (?, ?)",
            ('Snickers', 'American')
            )

cur.execute("INSERT INTO chocolates (name, country) VALUES (?, ?)",
            ('Fruit and Nut', 'British')
            )
# the cursor's execute() method allows us to execute 2 INSERT SQL statements to add to our chocolate table

connection.commit()
connection.close()
# commit the changes and close it 