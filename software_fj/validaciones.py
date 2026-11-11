"""Rutinas reutilizables para validar los datos antes de crear objetos."""

from decimal import Decimal, InvalidOperation
import re

from .excepciones import CalculoInvalidoError, DatoInvalidoError


_PATRON_CORREO = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_PATRON_ID = re.compile(r"^[A-Za-z0-9_-]{2,25}$")


def texto_obligatorio(valor: object, nombre: str, minimo: int = 2) -> str:
    """Exige texto real, no vacío ni formado únicamente por espacios."""
    if not isinstance(valor, str) or len(valor.strip()) < minimo:
        raise DatoInvalidoError(f"{nombre} debe tener mínimo {minimo} caracteres.")
    return valor.strip()


def identificador(valor: object) -> str:
    """Acepta identificadores de 2 a 25 caracteres alfanuméricos, _ o -."""
    if not isinstance(valor, str) or not _PATRON_ID.fullmatch(valor.strip()):
        raise DatoInvalidoError("Identificador inválido (2-25 caracteres: letras, números, _ o -).")
    return valor.strip()


def correo(valor: object) -> str:
    """Valida una dirección de correo con una comprobación básica."""
    if not isinstance(valor, str) or not _PATRON_CORREO.fullmatch(valor.strip()):
        raise DatoInvalidoError("Correo electrónico inválido.")
    return valor.strip().lower()


def telefono(valor: object) -> str:
    """Exige una secuencia de 7 a 15 dígitos, sin símbolos."""
    cadena = str(valor).strip() if not isinstance(valor, bool) else ""
    if not cadena.isdigit() or not 7 <= len(cadena) <= 15:
        raise DatoInvalidoError("Teléfono inválido: debe contener entre 7 y 15 dígitos.")
    return cadena


def entero_positivo(valor: object, nombre: str, maximo: int | None = None) -> int:
    """Evita aceptar valores flotantes, booleanos, cero o negativos."""
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise DatoInvalidoError(f"{nombre} debe ser un número entero positivo.")
    if maximo is not None and valor > maximo:
        raise DatoInvalidoError(f"{nombre} no puede superar {maximo}.")
    return valor


def decimal_valido(valor: object, nombre: str, permitir_cero: bool = False) -> Decimal:
    """Convierte números a Decimal y encadena errores de conversión."""
    if isinstance(valor, bool) or valor is None:
        raise CalculoInvalidoError(f"{nombre} debe ser un número válido.")
    try:
        resultado = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError) as original:
        raise CalculoInvalidoError(f"{nombre} no puede convertirse a un número.") from original
    if not resultado.is_finite():
        raise CalculoInvalidoError(f"{nombre} debe ser un número finito.")
    if resultado < 0 or (not permitir_cero and resultado == 0):
        condicion = "mayor o igual a cero" if permitir_cero else "mayor que cero"
        raise CalculoInvalidoError(f"{nombre} debe ser {condicion}.")
    return resultado


def porcentaje(valor: object, nombre: str) -> Decimal:
    """Limita descuentos e impuestos a porcentajes de 0 a 100."""
    numero = decimal_valido(valor, nombre, permitir_cero=True)
    if numero > 100:
        raise CalculoInvalidoError(f"{nombre} debe estar entre 0 y 100 %.")
    return numero
