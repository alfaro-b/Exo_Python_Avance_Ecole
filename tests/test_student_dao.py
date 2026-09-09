from daos.student_dao import StudentDao
from models.student import Student
from models.address import Address


student_dao = StudentDao()


# -------------------------
# TEST CREATE SANS ADRESSE
# -------------------------

student = Student(
    "Test",
    "Eleve",
    15
)

student_nbr = student_dao.create(student)

print("CREATE SANS ADRESSE")
print("Numéro étudiant créé :", student_nbr)
print(student)


# -------------------------
# TEST CREATE AVEC ADRESSE
# -------------------------

student_with_address = Student(
    "Paul",
    "Dupont",
    14
)

student_with_address.address = Address(
    "5 rue des Fleurs",
    "Bayonne",
    "64100"
)

student_nbr_with_address = student_dao.create(student_with_address)

print("\nCREATE AVEC ADRESSE")
print("Numéro étudiant créé :", student_nbr_with_address)
print(student_with_address)


# -------------------------
# TEST READ
# -------------------------

# read() attend actuellement un id_person
# Remplacer 1 par un id_person existant dans la BDD
student_read = student_dao.read(1)

print("\nREAD")
print(student_read)


# -------------------------
# TEST READ ALL
# -------------------------

students = student_dao.read_all()

print("\nREAD ALL")

for student in students:
    print(student)

# -------------------------
# TEST UPDATE
# -------------------------


# -------------------------
# TEST DELETE
# -------------------------
