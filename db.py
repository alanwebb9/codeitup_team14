import mysql.connector as conn
class dbManager:
    def databaseConnection(self):
        dbcon = conn.connect(
            user='b859561b02980e', 
            password='fdaa2895',
            host='eu-cdbr-west-02.cleardb.net',
            port = 3306,
            database = 'heroku_3993acd99918e69')
        return dbcon