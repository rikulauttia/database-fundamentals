import courses

courses.create_tables()

t1 = courses.create_teacher("Erkki Kaila")
t2 = courses.create_teacher("Antti Laaksonen")
t3 = courses.create_teacher("Matti Luukkainen")
t4 = courses.create_teacher("Emilia Oikarinen")
t5 = courses.create_teacher("Leena Salmela")

c1 = courses.create_course("Laskennan mallit", 7, [t1, t3])
c2 = courses.create_course("Ohjelmistotuotanto", 9, [t1, t2, t5])
c3 = courses.create_course("Ohjelmoinnin perusteet", 8, [t2, t5])
c4 = courses.create_course("Tietokantojen perusteet", 4, [t3, t4])
c5 = courses.create_course("Tietokoneen toiminta", 6, [t5])

s1 = courses.create_student("Heikki Lokki")
s2 = courses.create_student("Liisa Marttinen")
s3 = courses.create_student("Otto Nurmi")
s4 = courses.create_student("Esko Ukkonen")
s5 = courses.create_student("Arto Wikla")

courses.add_credits(s1, c1, "2020-01-10", 1)
courses.add_credits(s1, c2, "2021-05-02", 2)
courses.add_credits(s1, c4, "2021-04-20", 5)
courses.add_credits(s2, c1, "2021-03-10", 5)
courses.add_credits(s2, c2, "2022-09-08", 5)
courses.add_credits(s3, c3, "2022-09-10", 3)
courses.add_credits(s4, c3, "2022-11-01", 3)
courses.add_credits(s4, c4, "2020-11-29", 5)

courses.create_group("Basic-koodarit", [t1, t2], [s1, s2, s3, s5])
courses.create_group("Cobol-koodarit", [t4], [s2, s4, s5])
courses.create_group("Fortran-koodarit", [], [s5])
courses.create_group("PHP-koodarit", [t1, t2, t3], [s2, s3, s4, s5])

print(courses.courses_by_teacher("Leena Salmela"))
print(courses.credits_by_teacher("Leena Salmela"))
print(courses.courses_by_student("Esko Ukkonen"))

print(courses.credits_by_year(2020))
print(courses.credits_by_year(2021))
print(courses.credits_by_year(2022))

print(courses.grade_distribution("Ohjelmoinnin perusteet"))
print(courses.grade_distribution("Tietokoneen toiminta"))

print(courses.course_list())
print(courses.teacher_list())

print(courses.group_people("Basic-koodarit"))
print(courses.credits_in_groups())
print(courses.common_groups("Antti Laaksonen", "Otto Nurmi"))