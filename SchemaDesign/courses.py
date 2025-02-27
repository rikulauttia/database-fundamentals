import os
import os.path
import sqlite3

# poistaa tietokannan alussa (kätevä moduulin testailussa)
if os.path.exists("courses.db"):
    os.remove("courses.db")

db = sqlite3.connect("courses.db")
db.isolation_level = None

# luo tietokantaan tarvittavat taulut
def create_tables():
    db.execute("""
        CREATE TABLE teachers (
            id INTEGER PRIMARY KEY, 
            name TEXT
        )
    """)
    
    db.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            credits INTEGER
        )
    """)
    
    db.execute("""
        CREATE TABLE course_teachers (
            id INTEGER PRIMARY KEY,
            course_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY, 
            name TEXT
        )
    """)
    
    db.execute("""
        CREATE TABLE credits (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            date TEXT,
            grade INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE groups (
            id INTEGER PRIMARY KEY, 
            name TEXT
        )
    """)
    
    db.execute("""
        CREATE TABLE group_teachers (
            id INTEGER PRIMARY KEY,
            group_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    
    db.execute("""
        CREATE TABLE group_students (
            id INTEGER PRIMARY KEY,
            group_id INTEGER,
            student_id INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

# lisää opettajan tietokantaan
def create_teacher(name):
    cursor = db.execute("INSERT INTO teachers (name) VALUES (?)", [name])
    return cursor.lastrowid

# lisää kurssin tietokantaan
def create_course(name, credits, teacher_ids):
    cursor = db.execute("INSERT INTO courses (name, credits) VALUES (?, ?)", [name, credits])
    course_id = cursor.lastrowid
    
    for teacher_id in teacher_ids:
        db.execute("INSERT INTO course_teachers (course_id, teacher_id) VALUES (?, ?)", 
                  [course_id, teacher_id])
    
    return course_id

# lisää opiskelijan tietokantaan
def create_student(name):
    cursor = db.execute("INSERT INTO students (name) VALUES (?)", [name])
    return cursor.lastrowid

# antaa opiskelijalle suorituksen kurssista
def add_credits(student_id, course_id, date, grade):
    cursor = db.execute("""
        INSERT INTO credits (student_id, course_id, date, grade) 
        VALUES (?, ?, ?, ?)
    """, [student_id, course_id, date, grade])
    
    return cursor.lastrowid

# lisää ryhmän tietokantaan
def create_group(name, teacher_ids, student_ids):
    cursor = db.execute("INSERT INTO groups (name) VALUES (?)", [name])
    group_id = cursor.lastrowid
    
    for teacher_id in teacher_ids:
        db.execute("INSERT INTO group_teachers (group_id, teacher_id) VALUES (?, ?)", 
                  [group_id, teacher_id])
    
    for student_id in student_ids:
        db.execute("INSERT INTO group_students (group_id, student_id) VALUES (?, ?)", 
                  [group_id, student_id])
    
    return group_id

# hakee kurssit, joissa opettaja opettaa (aakkosjärjestyksessä)
def courses_by_teacher(teacher_name):
    cursor = db.execute("""
        SELECT c.name FROM courses c
        JOIN course_teachers ct ON c.id = ct.course_id
        JOIN teachers t ON t.id = ct.teacher_id
        WHERE t.name = ?
        ORDER BY c.name
    """, [teacher_name])
    
    return [row[0] for row in cursor.fetchall()]

# hakee opettajan antamien opintopisteiden määrän
def credits_by_teacher(teacher_name):
    cursor = db.execute("""
        SELECT SUM(co.credits) FROM credits cr
        JOIN courses co ON cr.course_id = co.id
        JOIN course_teachers ct ON co.id = ct.course_id
        JOIN teachers t ON ct.teacher_id = t.id
        WHERE t.name = ?
    """, [teacher_name])
    
    result = cursor.fetchone()[0]
    return 0 if result is None else result

# hakee opiskelijan suorittamat kurssit arvosanoineen (aakkosjärjestyksessä)
def courses_by_student(student_name):
    cursor = db.execute("""
        SELECT c.name, cr.grade FROM credits cr
        JOIN courses c ON cr.course_id = c.id
        JOIN students s ON cr.student_id = s.id
        WHERE s.name = ?
        ORDER BY c.name
    """, [student_name])
    
    return [(row[0], row[1]) for row in cursor.fetchall()]

# hakee tiettynä vuonna saatujen opintopisteiden määrän
def credits_by_year(year):
    cursor = db.execute("""
        SELECT SUM(c.credits) FROM credits cr
        JOIN courses c ON cr.course_id = c.id
        WHERE cr.date LIKE ?
    """, [f"{year}%"])
    
    result = cursor.fetchone()[0]
    return 0 if result is None else result

# hakee kurssin arvosanojen jakauman (järjestyksessä arvosanat 1-5)
def grade_distribution(course_name):
    result = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    cursor = db.execute("""
        SELECT cr.grade, COUNT(*) FROM credits cr
        JOIN courses c ON cr.course_id = c.id
        WHERE c.name = ?
        GROUP BY cr.grade
    """, [course_name])
    
    for grade, count in cursor.fetchall():
        result[grade] = count
    
    return result

# hakee listan kursseista (nimi, opettajien määrä, suorittajien määrä) (aakkosjärjestyksessä)
def course_list():
    cursor = db.execute("""
        SELECT c.name,
               (SELECT COUNT(*) FROM course_teachers ct WHERE ct.course_id = c.id),
               (SELECT COUNT(*) FROM credits cr WHERE cr.course_id = c.id)
        FROM courses c
        ORDER BY c.name
    """)
    
    return [(row[0], row[1], row[2]) for row in cursor.fetchall()]

# hakee listan opettajista kursseineen (aakkosjärjestyksessä opettajat ja kurssit)
def teacher_list():
    cursor = db.execute("""
        SELECT t.name, c.name
        FROM teachers t
        JOIN course_teachers ct ON t.id = ct.teacher_id
        JOIN courses c ON ct.course_id = c.id
        ORDER BY t.name, c.name
    """)
    
    result = []
    current_teacher = None
    current_courses = []
    
    for teacher_name, course_name in cursor.fetchall():
        if teacher_name != current_teacher:
            if current_teacher is not None:
                result.append((current_teacher, current_courses))
            current_teacher = teacher_name
            current_courses = [course_name]
        else:
            current_courses.append(course_name)
    
    if current_teacher is not None:
        result.append((current_teacher, current_courses))
    
    return result

# hakee ryhmässä olevat henkilöt (aakkosjärjestyksessä)
def group_people(group_name):
    cursor = db.execute("""
        SELECT t.name
        FROM group_teachers gt
        JOIN teachers t ON gt.teacher_id = t.id
        JOIN groups g ON gt.group_id = g.id
        WHERE g.name = ?
        
        UNION
        
        SELECT s.name
        FROM group_students gs
        JOIN students s ON gs.student_id = s.id
        JOIN groups g ON gs.group_id = g.id
        WHERE g.name = ?
        
        ORDER BY t.name
    """, [group_name, group_name])
    
    return [row[0] for row in cursor.fetchall()]

# hakee ryhmissä saatujen opintopisteiden määrät (aakkosjärjestyksessä)
def credits_in_groups():
    cursor = db.execute("""
        SELECT g.name, COALESCE(SUM(co.credits), 0)
        FROM groups g
        LEFT JOIN group_students gs ON g.id = gs.group_id
        LEFT JOIN credits cr ON gs.student_id = cr.student_id
        LEFT JOIN courses co ON cr.course_id = co.id
        GROUP BY g.name
        ORDER BY g.name
    """)
    
    return [(row[0], row[1]) for row in cursor.fetchall()]

# hakee ryhmät, joissa on tietty opettaja ja opiskelija (aakkosjärjestyksessä)
def common_groups(teacher_name, student_name):
    cursor = db.execute("""
        SELECT g.name
        FROM groups g
        JOIN group_teachers gt ON g.id = gt.group_id
        JOIN teachers t ON gt.teacher_id = t.id
        JOIN group_students gs ON g.id = gs.group_id
        JOIN students s ON gs.student_id = s.id
        WHERE t.name = ? AND s.name = ?
        ORDER BY g.name
    """, [teacher_name, student_name])
    
    return [row[0] for row in cursor.fetchall()]