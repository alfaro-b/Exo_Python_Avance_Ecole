#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

from business.school import School
from daos import address_dao
from daos.address_dao import AddressDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models import address
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # récupération de tous les cours de la BDD
    school.load_courses()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    # test création élève sans adresse
    # student = Student("Test", "Eleve", 15)
    # student_dao = StudentDao()
    # student_nbr = student_dao.create(student)
    # print("Numéro créé :", student_nbr)
    # print(student)

    # test création élève avec adresse
    # student = Student("Paul", "Dupont", 14)
    # student.address = Address("5 rue des Fleurs", "Bayonne", "64100")
    # student_dao = StudentDao()
    # student_dao.create(student)

    # test création adresse
    # address = Address("10 rue Test", "Bayonne", "64100")
    # address_dao =AddressDao()
    # id_address = address_dao.create(address)
    # print("ID créé : ", id_address)
    # print(address)

    # test création d'un enseignant
    # teacher = Teacher("Jean", "Martin", 35, date(2026, 9, 1))
    # teacher.address = Address("10 rue du Test", "Bayonne", "64100")
    # teacher_dao = TeacherDao()
    # id_teacher = teacher_dao.create(teacher)
    # print("ID enseignant :", id_teacher)
    # print(teacher)

    # Test création d'un cours
    #  course = Course("Python", date(2026, 9, 10), date(2026, 10, 10))
    # course_dao = CourseDao()
    # course_dao.create(course)


if __name__ == '__main__':
    main()
