"""Servicios polimórficos: salas, equipos y asesorías especializadas."""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from typing import overload

from .entidades import Entidad
from .excepciones import (
    CalculoInvalidoError,
    DatoInvalidoError,
    ServicioNoDisponibleError,
)
from .validaciones import decimal_valido, entero_positivo, porcentaje, texto_obligatorio


class Servicio(Entidad, ABC):
    """Servicio abstracto con datos comunes y cálculo porcentual reutilizable."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: object) -> None:
        super().__init__(codigo)
        self._nombre = texto_obligatorio(nombre, "Nombre del servicio")
        self._tarifa_hora = decimal_valido(tarifa_hora, "Tarifa por hora")
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> Decimal:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, disponible: bool) -> None:
        """Controla los cambios de disponibilidad del servicio."""
        if not isinstance(disponible, bool):
            raise DatoInvalidoError("Disponibilidad debe ser True o False.")
        self._disponible = disponible

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Valida las características particulares de cada servicio."""

    def _validar_comun(self, duracion: int) -> None:
        entero_positivo(duracion, "Duración")
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self.codigo} no está disponible.")

    def _total(self, subtotal: Decimal, descuento: object, impuesto: object) -> Decimal:
        """Aplica primero el descuento y luego el impuesto sobre el neto."""
        desc = porcentaje(descuento, "Descuento")
        iva = porcentaje(impuesto, "Impuesto")
        if subtotal <= 0 or not subtotal.is_finite():
            raise CalculoInvalidoError("El subtotal debe ser positivo y finito.")
        resultado = subtotal * (Decimal('1') - desc / 100)
        resultado *= Decimal('1') + iva / 100
        if not resultado.is_finite():
            raise CalculoInvalidoError("El costo calculado no es finito.")
        return resultado.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @overload
    def calcular_costo(self, duracion: int) -> Decimal: ...

    @overload
    def calcular_costo(self, duracion: int, descuento: object, impuesto: object = 0) -> Decimal: ...

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: object = 0, impuesto: object = 0) -> Decimal:
        """Método polimórfico; admite variantes con descuentos e impuestos."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción según el tipo específico de servicio."""


class ReservaSala(Servicio):
    """Reserva de salas: costo por hora y máximo ocho horas por turno."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: object, capacidad: int) -> None:
        super().__init__(codigo, nombre, tarifa_hora)
        self._capacidad = entero_positivo(capacidad, "Capacidad", maximo=500)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(self, duracion: int) -> None:
        self._validar_comun(duracion)
        entero_positivo(duracion, "Duración sala", maximo=8)

    def calcular_costo(self, duracion: int, descuento: object = 0, impuesto: object = 0) -> Decimal:
        self.validar_parametros(duracion)
        return self._total(self.tarifa_hora * duracion, descuento, impuesto)

    def describir(self) -> str:
        return f"Sala {self.codigo}: {self.nombre}, capacidad {self.capacidad}, $ {self.tarifa_hora}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: recargo fijo de preparación por alquiler."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: object, unidades: int, preparacion: object = 12000) -> None:
        super().__init__(codigo, nombre, tarifa_hora)
        self._unidades = entero_positivo(unidades, "Unidades", maximo=1000)
        self._preparacion = decimal_valido(preparacion, "Preparación", permitir_cero=True)

    @property
    def unidades(self) -> int:
        return self._unidades

    def validar_parametros(self, duracion: int) -> None:
        self._validar_comun(duracion)
        entero_positivo(duracion, "Duración equipo", maximo=72)

    def calcular_costo(self, duracion: int, descuento: object = 0, impuesto: object = 0) -> Decimal:
        self.validar_parametros(duracion)
        subtotal = self.tarifa_hora * duracion + self._preparacion
        return self._total(subtotal, descuento, impuesto)

    def describir(self) -> str:
        return f"Equipo {self.codigo}: {self.nombre}, {self.unidades} unidades, $ {self.tarifa_hora}/hora"


class AsesoriaEspecializada(Servicio):
    """Asesorías por hora, con un máximo de cuatro horas por sesión."""

    def __init__(self, codigo: str, nombre: str, tarifa_hora: object, especialidad: str) -> None:
        super().__init__(codigo, nombre, tarifa_hora)
        self._especialidad = texto_obligatorio(especialidad, "Especialidad", minimo=3)

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def validar_parametros(self, duracion: int) -> None:
        self._validar_comun(duracion)
        entero_positivo(duracion, "Duración asesoría", maximo=4)

    def calcular_costo(self, duracion: int, descuento: object = 0, impuesto: object = 0) -> Decimal:
        self.validar_parametros(duracion)
        return self._total(self.tarifa_hora * duracion, descuento, impuesto)

    def describir(self) -> str:
        return f"Asesoría {self.codigo}: {self.especialidad}, $ {self.tarifa_hora}/hora"
