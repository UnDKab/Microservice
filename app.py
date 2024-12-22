import psycopg2
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "users_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", 5432)
    )
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        age INT,
                        email VARCHAR(100)
                    )''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user[0], "name": user[1], "age": user[2], "email": user[3]})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'name' not in data or 'age' not in data or 'email' not in data:
        return jsonify({"error": "Bad request, missing data"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age, email) VALUES (%s, %s, %s) RETURNING id',
                   (data['name'], data['age'], data['email']))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": user_id, "name": data['name'], "age": data['age'], "email": data['email']}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    if user is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    if 'name' in data:
        cursor.execute('UPDATE users SET name = %s WHERE id = %s', (data['name'], user_id))
    if 'age' in data:
        cursor.execute('UPDATE users SET age = %s WHERE id = %s', (data['age'], user_id))
    if 'email' in data:
        cursor.execute('UPDATE users SET email = %s WHERE id = %s', (data['email'], user_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"id": user_id, "name": data.get('name', user[1]), "age": data.get('age', user[2]), "email": data.get('email', user[3])})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True, host='0.0.0.0')
