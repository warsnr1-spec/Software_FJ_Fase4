"""Punto de entrada. Ejecutar con --demo (simulación) o --menu (interactivo)."""

import argparse

from software_fj import Cliente, GestorSoftwareFJ, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.demo import imprimir_resumen, simular
from software_fj.excepciones import ErrorSoftwareFJ, DatoInvalidoError
from software_fj.registro import registro


def pedir_entero(mensaje: str) -> int:
    """Transforma entradas de consola y conserva el origen del error."""
    try:
        return int(input(mensaje).strip())
    except ValueError as original:
        raise DatoInvalidoError("Se esperaba un número entero.") from original


def mostrar_items(gestor: GestorSoftwareFJ) -> None:
    """Lista los objetos que permanecen únicamente en memoria."""
    for titulo, items in (
        ("CLIENTES", gestor.clientes),
        ("SERVICIOS", gestor.servicios),
        ("RESERVAS", gestor.reservas),
    ):
        print(f"\n{titulo}:")
        if not items:
            print("  (Sin registros)")
        for item in items:
            print("  -", item.describir())


def menu() -> None:
    """Permite usar manualmente el sistema sin depender de archivos de datos."""
    gestor = GestorSoftwareFJ()
    opciones = (
        "\nSOFTWARE FJ\n"
        "1. Registrar cliente\n"
        "2. Registrar servicio\n"
        "3. Crear reserva\n"
        "4. Confirmar reserva\n"
        "5. Procesar reserva\n"
        "6. Cancelar reserva\n"
        "7. Listar registros\n"
        "8. Habilitar o deshabilitar servicio\n"
        "9. Ejecutar demostración independiente\n"
        "0. Salir\n"
    )
    while True:
        try:
            print(opciones)
            eleccion = input("Seleccione una opción: ").strip()
            if eleccion == "0":
                print("Sesión finalizada. Los registros en memoria se descartan.")
                return
            if eleccion == "1":
                cliente = Cliente(
                    input("Código cliente: "), input("Nombre: "),
                    input("Correo: "), input("Celular: "),
                )
                gestor.agregar_cliente(cliente)
            elif eleccion == "2":
                clase = input("Tipo [sala/equipo/asesoria]: ").strip().lower()
                codigo = input("Código: ")
                nombre = input("Nombre: ")
                tarifa = input("Tarifa por hora (COP): ")
                if clase == "sala":
                    servicio = ReservaSala(codigo, nombre, tarifa, pedir_entero("Capacidad: "))
                elif clase == "equipo":
                    servicio = AlquilerEquipo(codigo, nombre, tarifa, pedir_entero("Unidades: "))
                elif clase == "asesoria":
                    servicio = AsesoriaEspecializada(codigo, nombre, tarifa, input("Especialidad: "))
                else:
                    raise DatoInvalidoError("Tipo de servicio desconocido.")
                gestor.agregar_servicio(servicio)
            elif eleccion == "3":
                reserva = gestor.crear_reserva(
                    input("Código reserva: "), input("Código cliente: "),
                    input("Código servicio: "), pedir_entero("Duración en horas: "),
                )
                print("Creada:", reserva.describir())
            elif eleccion == "4":
                gestor.confirmar_reserva(input("Código reserva: "))
            elif eleccion == "5":
                total = gestor.procesar_reserva(
                    input("Código reserva: "),
                    input("Descuento % [0]: ").strip() or "0",
                    input("Impuesto % [0]: ").strip() or "0",
                )
                print(f"Importe procesado: $ {total} COP")
            elif eleccion == "6":
                gestor.cancelar_reserva(input("Código reserva: "))
            elif eleccion == "7":
                mostrar_items(gestor)
            elif eleccion == "8":
                gestor.cambiar_disponibilidad(
                    input("Código servicio: "),
                    input("Habilitar [s/n]: ").strip().lower() == "s",
                )
            elif eleccion == "9":
                imprimir_resumen(simular())
            else:
                print("Opción inexistente. Seleccione un número de 0 a 9.")
                continue
            if eleccion not in ("3", "5", "7", "9"):
                print("Operación completada correctamente.")
        except (ErrorSoftwareFJ, ValueError) as error:
            registro.error("Error controlado en menú (%s): %s", type(error).__name__, error)
            print("No se completó la operación:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nSesión terminada por el usuario.")
            return
        except Exception:
            registro.exception("Error inesperado en menú")
            print("Ocurrió un problema inesperado; consulte el archivo de eventos.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sistema Software FJ - Fase 4 UNAD")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--demo", action="store_true", help="Ejecutar las 24 operaciones de demostración")
    grupo.add_argument("--menu", action="store_true", help="Abrir el menú interactivo")
    args = parser.parse_args()
    if args.menu:
        menu()
        return 0
    resultados = simular()
    imprimir_resumen(resultados)
    return 0 if all(item.aprobado for item in resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
