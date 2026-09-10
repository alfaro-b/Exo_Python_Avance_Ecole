# -*- coding: utf-8 -*-

"""
Classe Address
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Address:
    """Adresse d'une personne (enseignant ou élève)."""
    id: Optional[int] = field(default=None, init=False)
    street: str
    city: str
    postal_code: str
    # Modif postal_code en string au lieu de int
    # Modif dans MySQL passage en VARCHAR(5) au lieu de SMALLINT trop petit et pb avec cp en 0
    def __str__(self) -> str:
        return f"{self.street}, {self.postal_code} {self.city}"
