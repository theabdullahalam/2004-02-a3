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

#initialize_database()
# create a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or not 'first_name' in data or not 'last_name' in data or not 'dob' in data or not 'amount_due' in data:
        return jsonify({'error': 'Incomplete data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (first_name, last_name, dob, amount_due) VALUES (?, ?, ?, ?)',
                   (data['first_name'], data['last_name'], data['dob'], data['amount_due']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student created successfully'}), 201


# read all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()

    return jsonify([dict(student) for student in students]), 200


# read a specific student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify(dict(student)), 200


# Update a student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    cursor.execute('UPDATE students SET first_name = ?, last_name = ?, dob = ?, amount_due = ? WHERE student_id = ?',
                   (data['first_name'], data['last_name'], data['dob'], data['amount_due'], student_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully'}), 200


# Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
