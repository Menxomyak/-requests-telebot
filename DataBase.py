import sqlite3

def init_db():
    conn = sqlite3.connect('weather_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            temperature REAL,
            humidity INTEGER,
            description TEXT,
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_weather_request(city, user_id, temp, humid, desc):
    conn = sqlite3.connect('weather_history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather_requests (user_id, city, temperature, humidity, description) VALUES (?, ?, ?, ?, ?)",
                   (user_id, city, temp, humid, desc))
    conn.commit()
    conn.close()
