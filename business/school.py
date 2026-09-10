# -*- coding: utf-8 -*-

"""
Classe School
"""

from dataclasses import dataclass, field

from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models.course import Course
from models.teacher import Teacher
from models.student import Student


@dataclass
class School:
    """Couche métier de l'application de gestion d'une école,
    reprenant les cas d'utilisation et les spécifications fonctionnelles :
    courses : liste des cours existants
    teachers : liste des enseignants
    students : liste des élèves"""

    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        """Ajout du cours course à la liste des cours."""
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        """Ajout de l'enseignant teacher à la liste des enseignants."""
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        """Ajout de l'élève spécifié à la liste des élèves."""
        self.students.append(student)

    # Permet de chargeer toutes les infos des cours
    def load_courses(self) -> None:
        course_dao = CourseDao()
        teacher_dao = TeacherDao()
        student_dao = StudentDao()

        # récupération de tous les cours
        self.courses = course_dao.read_all()

        for course in self.courses:
            if course.id is None:
                continue

            # récupération de l'enseignant du cours
            id_teacher = course_dao.read_teacher_id(course.id)

            if id_teacher is not None:
                teacher = teacher_dao.read(id_teacher)

                if teacher is not None:
                    course.set_teacher(teacher)

            # récupération des élèves du cours
            students = student_dao.read_by_course_id(course.id)

            for student in students:
                course.add_student(student)

    def display_courses_list(self) -> None:
        """Affichage de la liste des cours avec pour chacun d'eux :
        leur enseignant
        la liste des élèves le suivant"""
        for course in self.courses:
            print(f"cours de {course}")
            for student in course.students_taking_it:
                print(f"- {student}")
            print()

    def display_teacher_courses(self, teacher: Teacher) -> None:
        """Affiche les cours enseignés par un enseignant."""
        print(f"\nCours enseignés par {teacher.first_name} {teacher.last_name} :")
        for course in self.courses:
            if course.teacher is not None and course.teacher.id == teacher.id:
                print(f"- {course}")

    def display_student_courses(self, student: Student) -> None:
        """Affiche les cours suivis par un élève"""
        print(f"\nCours suivis par {student.first_name} {student.last_name} :")
        for course in self.courses:
            for course_student in course.students_taking_it:
                if course_student.student_nbr == student.student_nbr:
                    print(f"- {course}")
                    break

    @staticmethod
    def get_course_by_id(id_course: int):
        course_dao: CourseDao = CourseDao()
        return course_dao.read(id_course)

    @staticmethod
    def get_teacher_by_id(id_teacher: int):
        teacher_dao: TeacherDao = TeacherDao()
        return teacher_dao.read(id_teacher)

    @staticmethod
    def get_student_by_nbr(student_nbr: int):
        student_dao: StudentDao = StudentDao()
        return student_dao.read(student_nbr)

