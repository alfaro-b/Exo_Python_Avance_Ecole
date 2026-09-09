# -*- coding: utf-8 -*-

"""
Classe abstraite générique Dao[T], dont hérite les classes de DAO de chaque entité
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Optional
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Dao[T](ABC):
    connection: ClassVar[pymysql.Connection] = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

    @abstractmethod
    def read_all(self) -> list[T]:
        """Récupère tous les objets correspondants à l'entité
           (ou None s'il n'a pu être trouvé)"""
        ...

    @abstractmethod
    def create(self, obj: T) -> int:
        """Crée l'entité en BD correspondant à l'objet obj

        :param obj: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué).
        """
        ...

    @abstractmethod
    def read(self, id_entity: int) -> Optional[T]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        ...

    @abstractmethod
    def update(self, obj: T) -> bool:
        """Met à jour en BD l'entité correspondant à obj, pour y correspondre

        :param obj: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...

    @abstractmethod
    def delete(self, obj: T) -> bool:
        """Supprime en BD l'entité correspondant à obj

        :param obj: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
