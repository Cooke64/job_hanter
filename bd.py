import sqlite3



def create_user(message):
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_id(
    id INTEGER
    )""")
    connect.commit()
    current_id = message.chat.id
    cursor.execute(f"SELECT id FROM user_id WHERE id = {current_id}")
    data = cursor.fetchone()
    if data is None:
        users_id = [message.chat.id]
        cursor.execute("INSERT INTO user_id VALUES(?);", users_id)
        connect.commit()


def delete_user(message):
    connect = sqlite3.connect('user.db')
    cursor = connect.cursor()
    current_id = message.chat.id
    cursor.execute(f"DELETE FROM user_id WHERE id = {current_id}")
    connect.commit()
