import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("--- Game Game Table ---")
cursor.execute('SELECT id, title, external_text, show_external, insta_text, show_insta FROM game_game')
for row in cursor:
    print(row)

conn.close()
