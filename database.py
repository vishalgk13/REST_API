from flask import g
import sqlite3
def connect_to_database():
    sql = sqlite3.connect("C:/Users/LENOVO/Desktop/employee/rest.db")
    sql.row_factory=sqlite3.Row
    return sql

def get_database():
    if not hasattr(g,"rest_db"):
        g.rest_db=connect_to_database()
    return g.rest_db

