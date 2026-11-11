"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Error de negocio controlado dentro de la aplicación."""


class DatoInvalidoError(ErrorSoftwareFJ):
    """Un dato recibido no supera las validaciones."""


class EntidadDuplicadaError(ErrorSoftwareFJ):
    """El identificador solicitado ya se encuentra registrado."""


class EntidadNoEncontradaError(ErrorSoftwareFJ):
    """No existe un objeto solicitado en las listas en memoria."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Un servicio no está habilitado para nuevas reservas."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Una reserva tiene parámetros incorrectos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operación contradice el estado actual de una reserva."""


class CalculoInvalidoError(ErrorSoftwareFJ):
    """No se puede calcular el precio por datos numéricos incorrectos."""
