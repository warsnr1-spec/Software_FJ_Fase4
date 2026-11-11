"""Cliente con propiedades encapsuladas y validaciones de datos."""

from .entidades import Entidad
from .validaciones import correo, telefono, texto_obligatorio


class Cliente(Entidad):
    """Cliente identificable, con atributos internos controlados."""

    def __init__(self, codigo: str, nombre: str, email: str, celular: str) -> None:
        super().__init__(codigo)
        self._nombre = texto_obligatorio(nombre, "Nombre")
        self._email = correo(email)
        self._celular = telefono(celular)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = texto_obligatorio(valor, "Nombre")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = correo(valor)

    @property
    def celular(self) -> str:
        return self._celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self._celular = telefono(valor)

    def describir(self) -> str:
        """Evita mostrar el correo y teléfono en listados públicos."""
        return f"Cliente {self.codigo}: {self.nombre}"
