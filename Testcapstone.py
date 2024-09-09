"""
CREATE USER 'capstone_user'@'localhost' IDENTIFIED BY '12345678';

GRANT ALL PRIVILEGES ON capstone.* TO 'capstone_user'@'localhost';
"""

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="capstone_user",
    password="12345678",
    database="capstone"
)
cursor = connection.cursor(dictionary=True)


def connectToDB():
    try:
        # update to connect database --
        
        if connection.is_connected():
            print("Connected to MySQL Server")
            return [True , connection]

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return [False, 0]
    
connectToDB()


# connection = connectToDB[1]
cursor = connection.cursor(dictionary=True)

# user (UserID	FName	LName	Email	Password)
# add a user 

query = "INSERT INTO user (FName, LName, Email, Password) VALUES (%s, %s, %s, %s)"

cursor.execute(query, ("capstone", "user2", "test@test.com", "test"))
connection.commit()
