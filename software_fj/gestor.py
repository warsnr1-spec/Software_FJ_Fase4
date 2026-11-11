"""Gestor del sistema: mantiene clientes, servicios y reservas en LISTAS."""

from functools import wraps
from typing import Callable, TypeVar, Any

from .cliente import Cliente
from .excepciones import EntidadDuplicadaError, EntidadNoEncontradaError, ErrorSoftwareFJ
from .registro import registro
from .reserva import Reserva
from .servicios import Servicio

T = TypeVar("T")


def auditar(funcion: Callable[..., T]) -> Callable[..., T]:
    """Captura, registra y propaga errores sin revelar información personal."""
    @wraps(funcion)
    def envoltura(*args: Any, **kwargs: Any) -> T:
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as error:
            registro.error("%s falló (%s): %s", funcion.__name__, type(error).__name__, error)
            raise
        except Exception:
            registro.exception("Error inesperado en %s", funcion.__name__)
            raise
        else:
            registro.info("Operación completada: %s", funcion.__name__)
            return resultado
    return envoltura


class GestorSoftwareFJ:
    """Almacena temporalmente objetos; nunca utiliza una base de datos."""

    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    @property
    def clientes(self) -> tuple[Cliente, ...]:
        return tuple(self._clientes)

    @property
    def servicios(self) -> tuple[Servicio, ...]:
        return tuple(self._servicios)

    @property
    def reservas(self) -> tuple[Reserva, ...]:
        return tuple(self._reservas)

    @auditar
    def agregar_cliente(self, cliente: Cliente) -> None:
        if not isinstance(cliente, Cliente):
            from .excepciones import DatoInvalidoError
            raise DatoInvalidoError("Se esperaba un objeto Cliente.")
        if any(item.codigo == cliente.codigo for item in self._clientes):
            raise EntidadDuplicadaError(f"El cliente {cliente.codigo} ya está registrado.")
        self._clientes.append(cliente)

    @auditar
    def agregar_servicio(self, servicio: Servicio) -> None:
        if not isinstance(servicio, Servicio):
            from .excepciones import DatoInvalidoError
            raise DatoInvalidoError("Se esperaba un objeto Servicio.")
        if any(item.codigo == servicio.codigo for item in self._servicios):
            raise EntidadDuplicadaError(f"El servicio {servicio.codigo} ya está registrado.")
        self._servicios.append(servicio)

    def _buscar_cliente(self, codigo: str) -> Cliente:
        for cliente in self._clientes:
            if cliente.codigo == codigo:
                return cliente
        raise EntidadNoEncontradaError(f"No existe el cliente {codigo}.")

    def _buscar_servicio(self, codigo: str) -> Servicio:
        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio
        raise EntidadNoEncontradaError(f"No existe el servicio {codigo}.")

    def _buscar_reserva(self, codigo: str) -> Reserva:
        for reserva in self._reservas:
            if reserva.codigo == codigo:
                return reserva
        raise EntidadNoEncontradaError(f"No existe la reserva {codigo}.")

    @auditar
    def crear_reserva(self, codigo: str, cliente_id: str, servicio_id: str, duracion: int) -> Reserva:
        """Crea y agrega la reserva solo después de completar las validaciones."""
        if any(item.codigo == codigo for item in self._reservas):
            raise EntidadDuplicadaError(f"La reserva {codigo} ya está registrada.")
        cliente = self._buscar_cliente(cliente_id)
        servicio = self._buscar_servicio(servicio_id)
        nueva_reserva = Reserva(codigo, cliente, servicio, duracion)
        self._reservas.append(nueva_reserva)
        return nueva_reserva

    @auditar
    def confirmar_reserva(self, codigo: str) -> None:
        self._buscar_reserva(codigo).confirmar()

    @auditar
    def cancelar_reserva(self, codigo: str) -> None:
        self._buscar_reserva(codigo).cancelar()

    @auditar
    def procesar_reserva(self, codigo: str, descuento: object = 0, impuesto: object = 0):
        return self._buscar_reserva(codigo).procesar(descuento, impuesto)

    @auditar
    def cambiar_disponibilidad(self, servicio_id: str, disponible: bool) -> None:
        self._buscar_servicio(servicio_id).cambiar_disponibilidad(disponible)
