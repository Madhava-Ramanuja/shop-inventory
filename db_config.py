import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql.railway.internal"),
        user="root",
        password=os.environ.get("DB_PASSWORD", "wEPOFWSbyQvPUpbtnhfJXGMDfrSffvao"),
        database=os.environ.get("DB_NAME", "railway"),
        port=3306
    )
