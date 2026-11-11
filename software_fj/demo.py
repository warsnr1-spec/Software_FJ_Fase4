"""Demostración reproducible de operaciones válidas e inválidas."""

from collections.abc import Callable
from dataclasses import dataclass

from .cliente import Cliente
from .excepciones import ErrorSoftwareFJ
from .gestor import GestorSoftwareFJ
from .registro import registro
from .servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


@dataclass(frozen=True)
class Resultado:
    numero: int
    operacion: str
    esperado: str
    observado: str
    aprobado: bool


def simular() -> list[Resultado]:
    """Realiza 24 operaciones; un error esperado cuenta como prueba superada."""
    gestor = GestorSoftwareFJ()
    resultados: list[Resultado] = []

    def operacion(nombre: str, accion: Callable[[], object], falla_esperada: bool = False) -> None:
        esperado = "ERROR CONTROLADO" if falla_esperada else "CORRECTO"
        try:
            valor = accion()
        except ErrorSoftwareFJ as error:
            registro.error("Operación de demostración %s: %s", nombre, error)
            observado = f"ERROR CONTROLADO ({type(error).__name__})"
            aprobado = falla_esperada
        except Exception as error:
            registro.exception("Error imprevisto en demostración: %s", nombre)
            observado = f"ERROR NO PREVISTO ({type(error).__name__})"
            aprobado = False
        else:
            detalle = valor.describir() if hasattr(valor, "describir") else str(valor)
            observado = "CORRECTO" + (f" [{detalle}]" if valor is not None else "")
            aprobado = not falla_esperada
        resultados.append(Resultado(len(resultados) + 1, nombre, esperado, observado, aprobado))

    operacion("Registrar cliente válido C001", lambda: gestor.agregar_cliente(Cliente("C001", "Ana Torres", "ana@ejemplo.com", "3001234567")))
    operacion("Rechazar cliente con nombre vacío", lambda: gestor.agregar_cliente(Cliente("C002", "  ", "x@ejemplo.com", "3001234567")), True)
    operacion("Registrar segundo cliente C003", lambda: gestor.agregar_cliente(Cliente("C003", "Luis Pérez", "luis@ejemplo.com", "3209876543")))
    operacion("Rechazar cliente duplicado C001", lambda: gestor.agregar_cliente(Cliente("C001", "Otra Persona", "otra@ejemplo.com", "3009998888")), True)
    operacion("Registrar sala SAL01", lambda: gestor.agregar_servicio(ReservaSala("SAL01", "Sala Ejecutiva", "50000", 15)))
    operacion("Rechazar equipo de tarifa negativa", lambda: gestor.agregar_servicio(AlquilerEquipo("EQ00", "Portátil", -20000, 3)), True)
    operacion("Registrar equipo EQ01", lambda: gestor.agregar_servicio(AlquilerEquipo("EQ01", "Computador portátil", "35000", 4)))
    operacion("Registrar asesoría ASE01", lambda: gestor.agregar_servicio(AsesoriaEspecializada("ASE01", "Asesoría profesional", "80000", "Seguridad informática")))
    operacion("Crear reserva válida R001", lambda: gestor.crear_reserva("R001", "C001", "SAL01", 2))
    operacion("Confirmar reserva R001", lambda: gestor.confirmar_reserva("R001"))
    operacion("Procesar R001 con descuento 10% e impuesto 19%", lambda: gestor.procesar_reserva("R001", 10, 19))
    operacion("Rechazar reserva de cliente inexistente", lambda: gestor.crear_reserva("R002", "C999", "SAL01", 1), True)
    operacion("Rechazar reserva de duración cero", lambda: gestor.crear_reserva("R003", "C001", "SAL01", 0), True)
    operacion("Crear reserva de asesoría R004", lambda: gestor.crear_reserva("R004", "C003", "ASE01", 1))
    operacion("Confirmar asesoría R004", lambda: gestor.confirmar_reserva("R004"))
    operacion("Cancelar asesoría R004", lambda: gestor.cancelar_reserva("R004"))
    operacion("Rechazar procesamiento de reserva cancelada", lambda: gestor.procesar_reserva("R004"), True)
    operacion("Deshabilitar servicio ASE01", lambda: gestor.cambiar_disponibilidad("ASE01", False))
    operacion("Rechazar reserva de servicio no disponible", lambda: gestor.crear_reserva("R005", "C001", "ASE01", 2), True)
    operacion("Rechazar descuento superior a 100%", lambda: gestor.servicios[0].calcular_costo(2, 120, 19), True)
    operacion("Crear reserva de equipo R006", lambda: gestor.crear_reserva("R006", "C003", "EQ01", 3))
    operacion("Rechazar cancelar reserva procesada R001", lambda: gestor.cancelar_reserva("R001"), True)
    operacion("Confirmar equipo R006", lambda: gestor.confirmar_reserva("R006"))
    operacion("Procesar alquiler de equipo R006", lambda: gestor.procesar_reserva("R006"))
    return resultados


def imprimir_resumen(resultados: list[Resultado]) -> None:
    print("\n" + "=" * 86)
    print("SOFTWARE FJ | SIMULACIÓN AUTOMÁTICA DE OPERACIONES")
    print("=" * 86)
    for resultado in resultados:
        veredicto = "APROBADA" if resultado.aprobado else "FALLIDA"
        print(f"{resultado.numero:02d}. {resultado.operacion}\n    Resultado: {resultado.observado} | {veredicto}")
    aprobados = sum(r.aprobado for r in resultados)
    print("-" * 86)
    print(f"Total: {len(resultados)} | Correctas según expectativa: {aprobados} | Fallidas: {len(resultados) - aprobados}")
    print("Eventos y errores registrados en logs/software_fj.log")
