import sqlite3
import random
import string
import time
import os

# Jokaisen elokuvan nimeksi valitaan satunnainen merkkijono, jossa on 8 merkkiä
def random_name():
    first_char = random.choice(string.ascii_uppercase)
    rest_chars = ''.join(random.choices(string.ascii_lowercase, k=7))
    return first_char + rest_chars

# tehdään tietokanta ja suoritetaan testit
def run_test(db_name, create_index_before_insert=False, create_index_before_query=False):
    if os.path.exists(db_name):
        os.remove(db_name)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Luodaan taulu Elokuvat, jossa on sarakkeet id, nimi ja vuosi.
    cursor.execute('''
    CREATE TABLE Elokuvat (
        id INTEGER PRIMARY KEY,
        nimi TEXT,
        vuosi INTEGER
    )
    ''')
    
    if create_index_before_insert:
        cursor.execute('CREATE INDEX vuosi_indeksi ON Elokuvat(vuosi)')
    
    insert_start_time = time.time()
    
    cursor.execute('BEGIN')
    
    for i in range(1000000):
        name = random_name()
        year = random.randint(1900, 2000)
        cursor.execute('INSERT INTO Elokuvat (nimi, vuosi) VALUES (?, ?)', (name, year))
    
    cursor.execute('COMMIT')
    
    insert_end_time = time.time()
    insert_time = insert_end_time - insert_start_time
    
    if create_index_before_query:
        cursor.execute('CREATE INDEX vuosi_indeksi ON Elokuvat(vuosi)')

    query_start_time = time.time()
    
    # suoritetaan 1000 kyselyä
    for i in range(1000):
        year = random.randint(1900, 2000)
        cursor.execute('SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?', (year,))
    
    query_end_time = time.time()
    query_time = query_end_time - query_start_time
    
    conn.close()
    
    # tietokantatiedoston koko testin jälkeen
    file_size = os.path.getsize(db_name) / (1024 * 1024)
    
    return insert_time, query_time, file_size

# Testi 1: Ei indexiä
print("Testi 1: Ei indexiä")
insert_time, query_time, file_size = run_test('elokuvat_testi1.db')
print(f"rivien lisäämiseen kuluva aika: {insert_time:.2f} sekunttia")
print(f"kyselyiden suoritukseen kuluva aika: {query_time:.2f} sekunttia")
print(f"tietokantatiedoston koko: {file_size:.2f} MB")
print()

# Testi 2: indeksi ennen rivien lisäämistä
print("Testi 2: indeksi ennen rivien lisäämistä")
insert_time, query_time, file_size = run_test('elokuvat_testi2.db', create_index_before_insert=True)
print(f"rivien lisäämiseen kuluva aika: {insert_time:.2f} sekunttia")
print(f"kyselyiden suoritukseen kuluva aika: {query_time:.2f} sekunttia")
print(f"tietokantatiedoston koko: {file_size:.2f} MB")
print()

# Testi 3: indeksi ennen kyselyiden suoritusta
print("Testi 3: indeksi ennen kyselyiden suoritusta")
insert_time, query_time, file_size = run_test('elokuvat_testi3.db', create_index_before_query=True)
print(f"rivien lisäämiseen kuluva aika: {insert_time:.2f} sekunttia")
print(f"kyselyiden suoritukseen kuluva aika: {query_time:.2f} sekunttia")
print(f"tietokantatiedoston koko: {file_size:.2f} MB")