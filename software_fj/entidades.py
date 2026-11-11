"""Contrato abstracto común a clientes, servicios y reservas."""

from abc import ABC, abstractmethod
from .validaciones import identificador


class Entidad(ABC):
    """Define el ID y la operación abstracta de descripción de entidades."""

    def __init__(self, codigo: str) -> None:
        self._codigo = identificador(codigo)

    @property
    def codigo(self) -> str:
        """ID de solo lectura: evita cambios después del registro."""
        return self._codigo

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad implementa su propia representación textual."""
