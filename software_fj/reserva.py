"""Reservas: integración cliente-servicio y transiciones de estado."""

from decimal import Decimal
from enum import Enum

from .cliente import Cliente
from .entidades import Entidad
from .excepciones import OperacionNoPermitidaError, ReservaInvalidaError, ErrorSoftwareFJ
from .registro import registro
from .servicios import Servicio
from .validaciones import entero_positivo


class EstadoReserva(str, Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"


class Reserva(Entidad):
    """Reserva de un cliente para un servicio durante un número de horas."""

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: int) -> None:
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Se requiere un Cliente registrado.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Se requiere un Servicio registrado.")
        self._duracion = entero_positivo(duracion, "Duración de la reserva")
        servicio.validar_parametros(self._duracion)
        self._cliente = cliente
        self._servicio = servicio
        self._estado = EstadoReserva.PENDIENTE
        self._total: Decimal | None = None

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def total(self) -> Decimal | None:
        return self._total

    def confirmar(self) -> None:
        """Solo puede confirmarse una reserva que todavía esté pendiente."""
        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se puede confirmar una reserva pendiente.")
        self._servicio.validar_parametros(self._duracion)
        self._estado = EstadoReserva.CONFIRMADA
        registro.info("Reserva %s confirmada", self.codigo)

    def cancelar(self) -> None:
        """No permite cancelar reservas ya procesadas o canceladas."""
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise OperacionNoPermitidaError("La reserva no puede cancelarse en su estado actual.")
        self._estado = EstadoReserva.CANCELADA
        registro.info("Reserva %s cancelada", self.codigo)

    def procesar(self, descuento: object = 0, impuesto: object = 0) -> Decimal:
        """Demuestra try/except/else/finally manteniendo el estado ante errores."""
        registro.info("Inicia procesamiento de reserva %s", self.codigo)
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError("La reserva debe estar confirmada antes de procesar.")
            total_calculado = self._servicio.calcular_costo(self._duracion, descuento, impuesto)
        except ErrorSoftwareFJ:
            registro.exception("Excepción controlada al procesar reserva %s", self.codigo)
            raise
        except Exception:
            registro.exception("Error inesperado al procesar reserva %s", self.codigo)
            raise
        else:
            self._total = total_calculado
            self._estado = EstadoReserva.PROCESADA
            registro.info("Reserva %s procesada por total $ %s", self.codigo, self._total)
            return self._total
        finally:
            registro.info("Finalizó intento de procesamiento de reserva %s", self.codigo)

    def describir(self) -> str:
        return (
            f"Reserva {self.codigo}: cliente {self.cliente.codigo}, "
            f"servicio {self.servicio.codigo}, {self.duracion} hora(s), estado {self.estado.value}"
        )
