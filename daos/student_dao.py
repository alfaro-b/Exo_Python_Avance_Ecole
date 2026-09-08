# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""
from models.address import Address
from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentDao(Dao[Student]):

    def read_all(self) -> list[Student]:
        students: list[Student] = []

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT
                    student.student_nbr,
                    person.id_person,
                    person.first_name,
                    person.last_name,
                    person.age,
                    address.id_address,
                    address.street,
                    address.city,
                    address.postal_code
                FROM student
                JOIN person ON student.id_person = person.id_person
                LEFT JOIN address ON person.id_address = address.id_address
            """
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            student = Student(
                record['first_name'], record['last_name'], record['age']
            )
            student.student_nbr = record['student_nbr']

            if record['id_address'] is not None:
                address = Address(
                    record['street'],
                    record['city'],
                    record['postal_code']
                )
                address.id = record['id_address']
                student.address = address

            students.append(student)

        return students

    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant au cours student

        :param student: à créer sous forme d'entité student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    def read(self, id_person: int) -> Optional[Student]:
        """Renvoit le student correspondant à l'entité dont l'id est id_person
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = ("""
                SELECT 
                    student.student_nbr,
                    person.id_person,
                    person.first_name,
                    person.last_name,
                    person.age,
                    address.id_address,
                    address.street,
                    address.city,
                    address.postal_code   
                FROM student 
                JOIN person ON student.id_person = person.id_person
                JOIN address ON address.id_address = person.id_address 
                WHERE student.id_person=%s""")
            cursor.execute(sql, (id_person,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(
                record['first_name'], record['last_name'], record['age'])
            student.student_nbr = record['student_nbr']
            if record['id_address'] is not None:
                address = Address(
                    record['street'], record['city'], record['postal_code']
                )
                address.id = record['id_address']
                student.address = address
        else:
            student = None

        return student

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre

        :param student: élève déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student

        :param student: élève dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True

    def read_by_course_id(self, id_course: int) -> list[Student]:
        """ Récupère la liste des étudiants en fonction de l'identifiant du cours"""
        students: list[Student] = []

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT
                    student.student_nbr,
                    person.id_person,
                    person.first_name,
                    person.last_name,
                    person.age,
                    address.id_address,
                    address.street,
                    address.city,
                    address.postal_code
                FROM takes
                JOIN student ON student.student_nbr = takes.student_nbr
                JOIN person ON person.id_person = student.id_person
                LEFT JOIN address ON address.id_address = person.id_address
                WHERE takes.id_course = %s
            """
            cursor.execute(sql, (id_course,))
            records = cursor.fetchall()

        for record in records:
            student = Student(
                record['first_name'],
                record['last_name'],
                record['age']
            )

            student.student_nbr = record['student_nbr']

            if record['id_address'] is not None:
                address = Address(
                    record['street'],
                    record['city'],
                    record['postal_code']
                )
                address.id = record['id_address']
                student.address = address

            students.append(student)

        return students