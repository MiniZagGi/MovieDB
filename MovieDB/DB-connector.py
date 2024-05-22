import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password123",
  database="MovieDB"
)

mycursor = mydb.cursor()


# Print all tables

# mycursor.execute("SHOW TABLES")
# for tables in mycursor:
#     print(tables)


# Print all fields names in table

# mycursor.execute("DESCRIBE Director")
# for tables in mycursor:
#     print(tables)


# Insert into Director table

sql = "INSERT INTO Director (FirstName, Lastname) VALUES (%s, %s)"
val = ("Nynne", "Awsome")
mycursor.execute(sql, val)

# Insert into Movie_Director

# sql = "INSERT INTO Movie_Director (Movie_MovieID, Director_DirectorID) VALUES (%s, %s)"
# val = (1, 2)
# mycursor.execute(sql, val)

mydb.commit()
