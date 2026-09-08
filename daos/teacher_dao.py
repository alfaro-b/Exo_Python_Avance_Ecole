# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""
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
        ...
        return 0

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
        ...
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: enseignant dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
