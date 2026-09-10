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

# Lecture d'un étudiant à partir de son student_nbr
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

student = student_dao.read(5)

if student is not None:
    print("\nAVANT UPDATE")
    print(student)

    student.first_name = "Paul Update"
    student.age = 16

    result = student_dao.update(student)

    print("\nUPDATE")
    print("Résultat :", result)

    student_updated = student_dao.read(5)

    print("\nAPRÈS UPDATE")
    print(student_updated)

# -------------------------
# TEST DELETE
# -------------------------

student = student_dao.read(5)

if student is not None:
    student_nbr = student.student_nbr

    print("\nAVANT DELETE")
    print(student)

    result = student_dao.delete(student)

    print("\nDELETE")
    print("Résultat :", result)

    student_deleted = student_dao.read(student_nbr)

    print("Après suppression :", student_deleted)

    # -------------------------
    # TEST ADD ADDRESS
    # -------------------------

    student = student_dao.read(1)

    if student is not None:
        print("\nAVANT AJOUT ADRESSE")
        print(student)

        address = Address("13 rue des pinsons", "Castanet", "31320")

        result = student_dao.add_address(student, address)

        print("\nAJOUT ADRESSE")
        print("Résultat :", result)

        student_updated = student_dao.read(1)

        print("\nAPRÈS AJOUT ADRESSE")
        print(student_updated)
