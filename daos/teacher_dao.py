# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""
from daos.address_dao import AddressDao
from models.address import Address
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):
    def read_all(self) -> list[Teacher]:
        teachers: list[Teacher] = []

        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT
                    teacher.id_teacher,
                    teacher.hiring_date,
                    person.first_name,
                    person.last_name,
                    person.age,
                    address.id_address,
                    address.street,
                    address.city,
                    address.postal_code
                FROM teacher
                JOIN person
                    ON teacher.id_person = person.id_person
                LEFT JOIN address
                    ON person.id_address = address.id_address
            """
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            teacher = Teacher(
                record['first_name'],
                record['last_name'],
                record['age'],
                record['hiring_date']
            )

            teacher.id = record['id_teacher']

            if record['id_address'] is not None:
                address = Address(
                    record['street'],
                    record['city'],
                    record['postal_code']
                )
                address.id = record['id_address']
                teacher.address = address

            teachers.append(teacher)

        return teachers

    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher

        :param teacher: à créer sous forme d'entité teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        # Création de l'adresse si l'enseignant en possède une
        if teacher.address is not None:
            address_dao = AddressDao()
            id_address = address_dao.create(teacher.address)
        else:
            id_address = None

        with Dao.connection.cursor() as cursor:

            # Création de la personne
            sql = """
                INSERT INTO person (first_name, last_name, age, id_address)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, id_address))

            id_person = cursor.lastrowid

            # Création de l'enseignant
            sql = """
                INSERT INTO teacher (hiring_date, id_person)
                VALUES (%s, %s)
            """

            cursor.execute(sql, (teacher.hiring_date, id_person))

            id_teacher = cursor.lastrowid

        Dao.connection.commit()

        teacher.id = id_teacher

        return id_teacher

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit le student correspondant à l'entité dont l'id est id_person
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = ("""
            SELECT 
                teacher.id_teacher,
                teacher.hiring_date,
                person.first_name,
                person.last_name,
                person.age,
                address.id_address,
                address.street,
                address.city,
                address.postal_code
            FROM teacher
            JOIN person ON person.id_person = teacher.id_person
            LEFT JOIN address ON address.id_address = person.id_address 
            WHERE teacher.id_teacher=%s""")
            # LEFT JOIN récupère quand même l'enseignant mêm si l'adresse est vide
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(
                record['first_name'],
                record['last_name'],
                record['age'],
                record['hiring_date']
            )

            teacher.id = record['id_teacher']

            if record['id_address'] is not None:
                address = Address(
                    record['street'],
                    record['city'],
                    record['postal_code']
                )
                address.id = record['id_address']
                teacher.address = address
        else:
            teacher = None

        return teacher

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: enseignant déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        if teacher.id is None:
            return False

        with Dao.connection.cursor() as cursor:
            # Mise à jour des informations de la personne
            sql = """
                UPDATE person
                JOIN teacher ON teacher.id_person = person.id_person
                SET person.first_name = %s,
                    person.last_name = %s,
                    person.age = %s
                WHERE teacher.id_teacher = %s
            """

            cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.id))

            # Mise à jour de la date d'embauche
            sql = """
                UPDATE teacher
                SET hiring_date = %s
                WHERE id_teacher = %s
            """

            cursor.execute(sql, (teacher.hiring_date, teacher.id))

        Dao.connection.commit()

        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: enseignant dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        if teacher.id is None:
            return False

        with Dao.connection.cursor() as cursor:
            # Récupération de l'id_person lié à l'enseignant
            sql = """
                SELECT id_person
                FROM teacher
                WHERE id_teacher = %s
            """
            cursor.execute(sql, (teacher.id,))
            record = cursor.fetchone()

            if record is None:
                return False

            id_person = record['id_person']

            # Retrait de l'enseignant des cours qu'il enseigne
            sql = """
                UPDATE course
                SET id_teacher = NULL
                WHERE id_teacher = %s
            """
            cursor.execute(sql, (teacher.id,))

            # Suppression de l'enseignant
            sql = """
                DELETE FROM teacher
                WHERE id_teacher = %s
            """
            cursor.execute(sql, (teacher.id,))

            # Suppression de la personne correspondante
            sql = """
                DELETE FROM person
                WHERE id_person = %s
            """
            cursor.execute(sql, (id_person,))

        Dao.connection.commit()

        # Suppression de son adresse
        if teacher.address is not None:
            address_dao = AddressDao()
            address_dao.delete(teacher.address)

        return True
