from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import random
from database.init_db import init_db

app = Flask(__name__)
DB_NAME = 'sensor_data.db'
TEMP_THRESHOLD = 40

# Insert random sensor data
def generate_random_data():
    temperature = round(random.uniform(25, 45), 2)  # Simulate temp 25–45
    humidity = round(random.uniform(30, 80), 2)     # Simulate humidity 30–80
    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (temperature, humidity, timestamp) VALUES (?, ?, ?)",
                   (temperature, humidity, timestamp))
    conn.commit()
    conn.close()

# Home route with dashboard
@app.route('/')
def index():
    return render_template('index.html')

# API to simulate new data + get latest record
@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    generate_random_data()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT temperature, humidity, timestamp FROM readings ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    data = {
        "temperature": row[0],
        "humidity": row[1],
        "timestamp": row[2],
        "alert": row[0] > TEMP_THRESHOLD
    }
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
