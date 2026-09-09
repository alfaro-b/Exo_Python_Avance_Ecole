# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

from models.teacher import Teacher


@dataclass
class CourseDao(Dao[Course]):
    def read_all(self) -> list[Course]:
        courses: list[Course] = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            course = Course(
                record['name'],
                record['start_date'],
                record['end_date']
            )
            course.id = record['id_course']
            courses.append(course)

        return courses

    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD
        """
        with Dao.connection.cursor() as cursor:
            sql = """
                INSERT INTO course (name, start_date, end_date)
                VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (course.name, course.start_date, course.end_date))

            id_course = cursor.lastrowid

        Dao.connection.commit()

        course.id = id_course

        return id_course

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        if course.id is None:
            return False

        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE course
                SET name = %s,
                    start_date = %s,
                    end_date = %s
                WHERE id_course = %s
            """

            cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id))

        Dao.connection.commit()

        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True

    def read_teacher_id(self, id_course: int) -> Optional[int]:
        """ Récupère l'enseignant d'un cours en fonction de l'identifiant du cours"""
        with Dao.connection.cursor() as cursor:
            sql = """
                SELECT id_teacher
                FROM course
                WHERE id_course = %s
            """
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()

        if record is not None:
            return record['id_teacher']

        return None

    def assign_teacher(self, course: Course, teacher: Teacher) -> bool:
        """Affecte un enseignant à un cours existant."""

        if course.id is None or teacher.id is None:
            return False

        with Dao.connection.cursor() as cursor:
            sql = """
                UPDATE course
                SET id_teacher = %s
                WHERE id_course = %s
            """

            cursor.execute(sql, (teacher.id, course.id))

        Dao.connection.commit()

        course.set_teacher(teacher)

        return True
