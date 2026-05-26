import mysql.connector 

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Medtronic2026!", 
        database="universidad"
    )