import mysql.connector
# Tests if a tuple is modifyed if retuned with an index
# If index is used it returns a str
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")

def testings(uinput):
    print(f"Inside {type(uinput)}")
    return uinput[0]

resualt = testings(thistuple)
print(f"Outside {type(resualt)}")

# What is the output of this tuple
output = [('DVD',), ('Blu-ray',), ('4K-Blu-ray',)]

for x in output:
    print(type(x))
    print(x[0])

somehting = (1,)

if somehting[0] is 1:
    print('yes')



def is_media_backed_up(cursor, movie_id, media_type_id):
    select_query = """
        SELECT `IsBackedUp` FROM `Movie_MediaType` WHERE `Movie_MovieID` = %s AND `MediaType_MediaTypeID` = %s
    """
    cursor.execute(select_query, (movie_id, media_type_id))
    resultTuple = cursor.fetchone()
    # Check if backed up or not. If no entry return None

    # Returns true or false if there is a row in table else return None
    if resultTuple != None:
        # Converts tuple to True or False and returns it
        result = bool(resultTuple[0])
        return result
    else:
         # returns None as resualt does not conatin true or false - a row with matching values does not exsit
         return None 
    print(resultTuple)
            

# Database connection setup
db_connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="MovieDB"
)
cursor = db_connection.cursor()

print(is_media_backed_up(cursor, 4, 2))


cursor.close()
db_connection.close()