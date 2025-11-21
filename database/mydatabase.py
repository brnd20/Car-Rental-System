import mysql.connector

#Connection haaton database
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="car_rental_db"
        )

    #function na ginagamit ha iba nga files
    def get_connection(self):
        return self.connection