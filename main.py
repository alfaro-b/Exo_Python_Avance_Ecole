#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School
from daos.student_dao import StudentDao
from models.student import Student


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

# test création élève
    student = Student("Test", "Eleve", 15)

    student_dao = StudentDao()
    student_nbr = student_dao.create(student)

    print("Numéro créé :", student_nbr)
    print(student)


if __name__ == '__main__':
    main()
