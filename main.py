import json
import sqlite3
import eel

globals()['flag'] = False


@eel.expose
def save_to_database(data):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        # Вставка новых данных
        for item in data:
            cursor.execute("INSERT OR REPLACE INTO machines (text1, text2, x, y, angle) VALUES (?, ?, ?, ?, ?)",
                           (item['text1'], item['text2'], item['x'], item['y'], item['angle']))
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
        cursor.execute("SELECT text1, text2, x, y, angle FROM machines")
        rows = cursor.fetchall()
        data = [{"text1": row[0], "text2": row[1], "x": row[2], "y": row[3], "angle": row[4]} for row in rows]
        conn.close()
        return json.dumps(data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return json.dumps([])


@eel.expose
def record_maintenance_event(text1, text2, x, y, angle, event_type, description):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM machines WHERE text1 = ? AND text2 = ? AND x = ? AND y = ? AND angle = ?",
                       (text1, text2, x, y, angle))
        result = cursor.fetchone()
        if result:
            machine_id = result[0]
            cursor.execute("INSERT INTO maintenance_history (machine_id, event_type, description) VALUES (?, ?, ?)",
                           (machine_id, event_type, description))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        print(f"Error recording maintenance event: {e}")
        return False


@eel.expose
async def get_maintenance_history(text1, text2, x, y, angle):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.event_type, m.event_date, m.description
            FROM maintenance_history m
            JOIN machines mc ON m.machine_id = mc.id
            WHERE mc.text1 = ? AND mc.text2 = ? AND mc.x = ? AND mc.y = ? AND mc.angle = ?
            ORDER BY m.event_date DESC
        """, (text1, text2, x, y, angle))
        rows = cursor.fetchall()
        history = [{'event_type': row[0], 'event_date': row[1], 'description': row[2]} for row in rows]
        conn.close()
        return json.dumps(history)
    except Exception as e:
        print(f"Error retrieving maintenance history: {e}")
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
