import mysql.connector as conn
class dbManager:
    def databaseConnection(self):
        dbcon = conn.connect(
            user='root', 
            password='',
            host='localhost',
            database = 'healthcare')
        return dbcon