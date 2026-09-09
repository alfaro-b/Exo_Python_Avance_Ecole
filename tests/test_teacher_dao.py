from datetime import date

from daos.teacher_dao import TeacherDao
from models.teacher import Teacher
from models.address import Address


teacher_dao = TeacherDao()


# -------------------------
# TEST CREATE
# -------------------------

teacher = Teacher(
    "Jean",
    "Martin",
    35,
    date(2026, 9, 1)
)

teacher.address = Address(
    "10 rue du Test",
    "Bayonne",
    "64100"
)

id_teacher = teacher_dao.create(teacher)

print("CREATE")
print("ID enseignant :", id_teacher)
print(teacher)


# -------------------------
# TEST READ
# -------------------------

teacher = teacher_dao.read(id_teacher)

print("\nREAD")
print(teacher)


# -------------------------
# TEST READ ALL
# -------------------------

teachers = teacher_dao.read_all()

print("\nREAD ALL")

for teacher in teachers:
    print(teacher)


# -------------------------
# TEST UPDATE
# -------------------------

teacher = teacher_dao.read(7)

if teacher is not None:
    print("\nAVANT UPDATE")
    print(teacher)

    teacher.first_name = "Prénom Update"
    teacher.hiring_date = date(2026, 9, 9)

    result = teacher_dao.update(teacher)

    print("\nUPDATE")
    print("Résultat :", result)

    # Nouvelle lecture depuis la BDD pour vérifier
    teacher_updated = teacher_dao.read(7)

    print("\nAPRÈS UPDATE")
    print(teacher_updated)

# -------------------------
# TEST DELETE
# -------------------------
