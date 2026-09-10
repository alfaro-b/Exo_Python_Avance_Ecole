#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # récupération de tous les cours de la BDD
    school.load_courses()

    print("""
    Qui êtes-vous ?
    1 - Élève
    2 - Enseignant
    3 - Directeur
    0 - Quitter
    """)

    choice = input("Votre choix : ")

    # -------------------------
    # ÉLÈVE
    # -------------------------
    if choice == "1":

        student_nbr = int(input("Numéro étudiant : "))
        student = school.get_student_by_nbr(student_nbr)

        if student is None:
            print("Élève introuvable.")
        else:
            school.display_student_courses(student)

    # -------------------------
    # ENSEIGNANT
    # -------------------------
    elif choice == "2":

        id_teacher = int(input("Identifiant enseignant : "))
        teacher = school.get_teacher_by_id(id_teacher)

        if teacher is None:
            print("Enseignant introuvable.")
        else:
            school.display_teacher_courses(teacher)

    # -------------------------
    # DIRECTEUR
    # -------------------------
    elif choice == "3":
        print("\nListe de tous les cours :")
        school.display_courses_list()

    # -------------------------
    # QUITTER
    # -------------------------
    elif choice == "0":
        print("Au revoir.")

    else:
        print("Choix invalide.")


if __name__ == '__main__':
    main()
