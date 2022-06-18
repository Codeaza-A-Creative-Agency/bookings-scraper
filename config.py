import json
import mysql.connector

def connection():
    db = mysql.connector.connect(
        host=configuration["db_host"],
        user=configuration["db_username"],
        # charset='utf8mb4',
        password=configuration["db_password"],
        database=configuration["db_name"]
    )
    if db.is_connected():
        print("You're connected to database!")
    cursor = db.cursor()
    return cursor, db


def close_connection(cursor, db):
    cursor.close()
    db.close()
    if not db.is_connected():
        print("MySQL connection is closed")

# loading DB credentials
with open("config.json","r") as file:
    configuration = json.load(file)
