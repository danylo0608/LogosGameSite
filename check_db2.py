import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("--- External Text Values ---")
cursor.execute('SELECT DISTINCT external_text FROM game_game WHERE external_text IS NOT NULL')
for row in cursor:
    print(repr(row[0]))

print("\n--- Insta Text Values ---")
cursor.execute('SELECT DISTINCT insta_text FROM game_game WHERE insta_text IS NOT NULL')
for row in cursor:
    print(repr(row[0]))

conn.close()
