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
            # Проверка наличия записи с такими же text1 и text2
            cursor.execute("SELECT id FROM machines WHERE text1 = ? AND text2 = ?", (item['text1'], item['text2']))
            result = cursor.fetchone()

            if result:
                # Если запись существует, обновляем координаты, угол и статус
                machine_id = result[0]
                cursor.execute("UPDATE machines SET x = ?, y = ?, angle = ?, status = ? WHERE id = ?",
                               (item['x'], item['y'], item['angle'], item['status'], machine_id))
            else:
                # Если записи нет, добавляем новую запись
                cursor.execute("INSERT INTO machines (text1, text2, x, y, angle, status) VALUES (?, ?, ?, ?, ?, ?)",
                               (item['text1'], item['text2'], item['x'], item['y'], item['angle'], item['status']))

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
        cursor.execute("SELECT text1, text2, x, y, angle, status FROM machines")
        rows = cursor.fetchall()
        data = [{"text1": row[0], "text2": row[1], "x": row[2], "y": row[3], "angle": row[4], "status": row[5]} for row
                in rows]
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
            if event_type == 'breakdown':
                cursor.execute("UPDATE machines SET status = 'needs_repair' WHERE id = ?", (machine_id,))
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
def get_maintenance_history_by_inventory_number(inventory_number):
    print(inventory_number)
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.event_type, m.event_date, m.description
            FROM maintenance_history m
            JOIN machines mc ON m.machine_id = mc.id
            WHERE mc.text1 = ?
            ORDER BY m.event_date DESC
        """, (str(inventory_number),))
        rows = cursor.fetchall()
        history = [{'event_type': row[0], 'event_date': row[1], 'description': row[2]} for row in rows]
        conn.close()
        return json.dumps(history)
    except Exception as e:
        print(f"Error retrieving maintenance history by inventory number: {e}")
        return json.dumps([])


@eel.expose
def get_inventory_numbers():
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT text1 FROM machines")
        rows = cursor.fetchall()
        inventory_numbers = [str(row[0]) for row in rows]
        conn.close()
        return json.dumps(inventory_numbers)
    except Exception as e:
        print(f"Error retrieving inventory numbers: {e}")
        return json.dumps([])


@eel.expose
def delete_machine(text1, text2, x, y, angle):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM machines WHERE text1 = ? AND text2 = ? AND x = ? AND y = ? AND angle = ?",
                       (text1, text2, x, y, angle))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting machine: {e}")
        return False


@eel.expose
def get_machine_counts():
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM machines GROUP BY status")
        rows = cursor.fetchall()
        counts = {row[0]: row[1] for row in rows}
        conn.close()
        return json.dumps(counts)
    except Exception as e:
        print(f"Error retrieving machine counts: {e}")
        return json.dumps({})


@eel.expose
def update_machine_status(text1, text2, x, y, angle, status):
    try:
        conn = sqlite3.connect('machines.sl3')
        cursor = conn.cursor()
        cursor.execute("UPDATE machines SET status = ? WHERE text1 = ? AND text2 = ? AND x = ? AND y = ? AND angle = ?",
                       (status, text1, text2, x, y, angle))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating machine status: {e}")
        return False


if __name__ == "__main__":
    eel.init('web')
    try:
        eel.start('index.html', size=(1920, 1080))
    except OSError as e:
        if "Can't find Google Chrome/Chromium installation" in str(e):
            eel.start('index.html', mode="browser")
        else:
            print(f"Error: {e}")
