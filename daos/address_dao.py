# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressDao(Dao[Address]):
    def read_all(self) -> list[Address]:
        addresses: list[Address] = []

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address"
            cursor.execute(sql)
            records = cursor.fetchall()

        for record in records:
            address = Address(
                record['street'],
                record['city'],
                record['postal_code']
            )
            address.id = record['id_address']
            addresses.append(address)

        return addresses

    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address

        :param address: à créer sous forme d'entité address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...
        return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoit l'adresse correspondant à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = ("""SELECT * 
            FROM address
            WHERE id_address=%s""")
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(
                record['id_address'],
                record['street'],
                record['city'],
                record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Address correspondant à address, pour y correspondre

        :param address: adresse déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Address correspondant à address

        :param address: adresse dont l'entité Address correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
