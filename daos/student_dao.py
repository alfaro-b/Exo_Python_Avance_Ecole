# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""
from daos.address_dao import AddressDao
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
        """Crée en BD l'entité Student correspondant à student
        :param student: à créer sous forme d'entité student en BD
        :return: l'id de l'entité insérée en BD
        """
        # 1. Création de l'adresse si l'élève en possède une
        if student.address is not None:
            address_dao = AddressDao()
            id_address = address_dao.create(student.address)
        else:
            id_address = None

        with Dao.connection.cursor() as cursor:

            # 2. Création de la personne
            sql = """
                INSERT INTO person (first_name, last_name, age, id_address)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (student.first_name, student.last_name, student.age, id_address))

            # Récupération de l'id_person généré par MySQL
            id_person = cursor.lastrowid

            # 3. Création de l'étudiant
            sql = """
                INSERT INTO student (id_person)
                VALUES (%s)
            """

            cursor.execute(sql, (id_person,))

            # student_nbr est AUTO_INCREMENT
            student_nbr = cursor.lastrowid

        Dao.connection.commit()

        # Mise à jour de l'objet Python
        student.student_nbr = student_nbr

        return student_nbr

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoie le student correspondant à l'entité dont l'id est student_nbr
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
                LEFT JOIN address ON address.id_address = person.id_address 
                WHERE student.student_nbr=%s""")
            cursor.execute(sql, (student_nbr,))
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
        if student.student_nbr is None:
            return False

        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE person
                JOIN student ON student.id_person = person.id_person
                SET person.first_name = %s,
                    person.last_name = %s,
                    person.age = %s
                WHERE student.student_nbr = %s
            """

            cursor.execute(sql, (student.first_name, student.last_name, student.age, student.student_nbr))

        Dao.connection.commit()

        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student
        :param student: élève dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        if student.student_nbr is None:
            return False

        with Dao.connection.cursor() as cursor:
            # Récupération de l'id_person lié à l'étudiant
            sql = """
                SELECT id_person
                FROM student
                WHERE student_nbr = %s
            """
            cursor.execute(sql, (student.student_nbr,))
            record = cursor.fetchone()

            if record is None:
                return False

            id_person = record['id_person']

            # Suppression des inscriptions de l'étudiant aux cours
            sql = """
                DELETE FROM takes
                WHERE student_nbr = %s
            """
            cursor.execute(sql, (student.student_nbr,))

            # Suppression de l'étudiant
            sql = """
                DELETE FROM student
                WHERE student_nbr = %s
            """
            cursor.execute(sql, (student.student_nbr,))

            # Suppression de la personne correspondante
            sql = """
                DELETE FROM person
                WHERE id_person = %s
            """
            cursor.execute(sql, (id_person,))

        Dao.connection.commit()

        # Suppression de son adresse si elle existe
        if student.address is not None:
            address_dao = AddressDao()
            address_dao.delete(student.address)

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
