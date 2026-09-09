from datetime import date

from daos.course_dao import CourseDao
from daos.teacher_dao import TeacherDao
from models.course import Course


course_dao = CourseDao()
teacher_dao = TeacherDao()


# -------------------------
# TEST CREATE
# -------------------------

course = Course(
    "Python",
    date(2026, 9, 10),
    date(2026, 10, 10)
)

id_course = course_dao.create(course)

print("CREATE")
print("ID cours :", id_course)
print(course)


# -------------------------
# TEST READ
# -------------------------

course = course_dao.read(id_course)

print("\nREAD")
print(course)


# -------------------------
# TEST READ ALL
# -------------------------

courses = course_dao.read_all()

print("\nREAD ALL")

for course in courses:
    print(course)


# -------------------------
# TEST ASSIGN TEACHER
# -------------------------

# On récupère un enseignant existant en BDD
teacher = teacher_dao.read(1)

print("\nASSIGN TEACHER")
print("Avant affectation :", course)

if course is not None and teacher is not None:
    result = course_dao.assign_teacher(course, teacher)

    print("Affectation réussie :", result)
    print("Après affectation :", course)


# -------------------------
# TEST UPDATE
# -------------------------

course = course_dao.read(9)

if course is not None:
    course.name = "Python avancé"
    course.end_date = date(2026, 9, 11)

    result = course_dao.update(course)

    print("\nUPDATE")
    print("Résultat :", result)
    print(course)


# -------------------------
# TEST DELETE
# -------------------------

course = course_dao.read(9)

if course is not None:

    result = course_dao.delete(course)

    print("\nDELETE")
    print("Résultat :", result)

    # Vérification en BDD
    course_deleted = course_dao.read(9)
    print("Cours après suppression :", course_deleted)