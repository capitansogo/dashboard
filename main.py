import json
import sqlite3
import eel

globals()['flag'] = False


@eel.expose
def save_to_database(data):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        for item in data:
            cursor.execute("INSERT INTO machines (text1, text2, x, y) VALUES (?, ?, ?, ?)",
                           (item['text1'], item['text2'], item['x'], item['y']))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


@eel.expose
def load_from_database():
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("SELECT text1, text2, x, y FROM machines")
        rows = cursor.fetchall()
        data = [{"text1": row[0], "text2": row[1], "x": row[2], "y": row[3]} for row in rows]
        conn.close()
        return json.dumps(data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return json.dumps([])


if __name__ == "__main__":
    eel.init('web')
    try:
        eel.start('index.html', size=(1920, 1080))
    except OSError as e:
        if "Can't find Google Chrome/Chromium installation" in str(e):
            eel.start('index.html', mode="browser")
        else:
            print(f"Error: {e}")
