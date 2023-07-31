from flask import Flask, request, jsonify, make_response
import sqlite3

app = Flask(__name__)

# Helper function to create a connection to the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database table
def initialize_database():
    conn = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()

initialize_database()



