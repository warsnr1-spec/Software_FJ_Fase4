"""Pruebas unitarias sin dependencias externas ni bases de datos."""

import unittest
from decimal import Decimal

from software_fj import (
    Cliente, GestorSoftwareFJ, ReservaSala, AlquilerEquipo,
    AsesoriaEspecializada, EstadoReserva, Reserva,
)
from software_fj.demo import simular
from software_fj.entidades import Entidad
from software_fj.excepciones import (
    CalculoInvalidoError, DatoInvalidoError, EntidadDuplicadaError,
    EntidadNoEncontradaError, OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)


class PruebasCliente(unittest.TestCase):
    def test_registra_cliente_valido(self):
        c = Cliente("C001", "Ana María", "ANA@EJEMPLO.COM", "3001234567")
        self.assertEqual(c.email, "ana@ejemplo.com")
        self.assertEqual(c.codigo, "C001")

    def test_nombre_vacio(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("C001", "  ", "ana@ejemplo.com", "3001234567")

    def test_correo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("C001", "Ana", "sin-arroba", "3001234567")

    def test_telefono_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("C001", "Ana", "ana@ejemplo.com", "3AAB")

    def test_id_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("#", "Ana", "ana@ejemplo.com", "3001234567")

    def test_encapsulacion_setter(self):
        c = Cliente("C001", "Ana", "ana@ejemplo.com", "3001234567")
        with self.assertRaises(DatoInvalidoError):
            c.email = "incorrecto"
        self.assertEqual(c.email, "ana@ejemplo.com")

    def test_entidad_es_abstracta(self):
        with self.assertRaises(TypeError):
            Entidad("E001")


class PruebasServicios(unittest.TestCase):
    def setUp(self):
        self.sala = ReservaSala("S001", "Sala VIP", "50000", 20)
        self.equipo = AlquilerEquipo("E001", "Portátil", "35000", 4)
        self.asesoria = AsesoriaEspecializada("A001", "Asesoría TI", "80000", "Seguridad")

    def test_sala_costo_base(self):
        self.assertEqual(self.sala.calcular_costo(2), Decimal("100000.00"))

    def test_sala_costo_con_descuento_e_impuesto(self):
        self.assertEqual(self.sala.calcular_costo(2, 10, 19), Decimal("107100.00"))

    def test_equipo_incluye_preparacion(self):
        self.assertEqual(self.equipo.calcular_costo(2), Decimal("82000.00"))

    def test_asesoria_precio(self):
        self.assertEqual(self.asesoria.calcular_costo(1), Decimal("80000.00"))

    def test_sala_duracion_maxima(self):
        with self.assertRaises(DatoInvalidoError):
            self.sala.calcular_costo(9)

    def test_asesoria_duracion_maxima(self):
        with self.assertRaises(DatoInvalidoError):
            self.asesoria.calcular_costo(5)

    def test_equipo_duracion_maxima(self):
        with self.assertRaises(DatoInvalidoError):
            self.equipo.calcular_costo(73)

    def test_descuento_fuera_de_rango(self):
        with self.assertRaises(CalculoInvalidoError):
            self.sala.calcular_costo(2, 150)

    def test_impuesto_invalido(self):
        with self.assertRaises(CalculoInvalidoError):
            self.sala.calcular_costo(2, 0, "texto")

    def test_tarifa_negativa(self):
        with self.assertRaises(CalculoInvalidoError):
            AlquilerEquipo("E002", "Equipo", "-2", 2)

    def test_disponibilidad(self):
        self.sala.cambiar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.calcular_costo(2)

    def test_polimorfismo_de_descripcion(self):
        servicios = [self.sala, self.equipo, self.asesoria]
        descripciones = [servicio.describir() for servicio in servicios]
        self.assertTrue(descripciones[0].startswith("Sala"))
        self.assertTrue(descripciones[1].startswith("Equipo"))
        self.assertTrue(descripciones[2].startswith("Asesoría"))

    def test_no_acepta_duracion_booleana(self):
        with self.assertRaises(DatoInvalidoError):
            self.sala.calcular_costo(True)

    def test_descuento_infinito(self):
        with self.assertRaises(CalculoInvalidoError):
            self.sala.calcular_costo(1, "Infinity")

    def test_encadenamiento_de_excepcion(self):
        with self.assertRaises(CalculoInvalidoError) as contexto:
            self.sala.calcular_costo(1, "NO_NUMERO")
        self.assertIsNotNone(contexto.exception.__cause__)


class PruebasReservas(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("C001", "Ana", "ana@ejemplo.com", "3001234567")
        self.servicio = ReservaSala("S001", "Sala", "50000", 20)
        self.reserva = Reserva("R001", self.cliente, self.servicio, 2)

    def test_reserva_inicialmente_pendiente(self):
        self.assertEqual(self.reserva.estado, EstadoReserva.PENDIENTE)

    def test_confirmar_y_procesar(self):
        self.reserva.confirmar()
        total = self.reserva.procesar(10, 19)
        self.assertEqual(total, Decimal("107100.00"))
        self.assertEqual(self.reserva.estado, EstadoReserva.PROCESADA)

    def test_no_procesar_pendiente(self):
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()
        self.assertEqual(self.reserva.estado, EstadoReserva.PENDIENTE)

    def test_cancelar_pendiente(self):
        self.reserva.cancelar()
        self.assertEqual(self.reserva.estado, EstadoReserva.CANCELADA)

    def test_no_procesar_cancelada(self):
        self.reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()

    def test_no_cancelar_procesada(self):
        self.reserva.confirmar()
        self.reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    def test_error_en_calculo_no_cambia_estado(self):
        self.reserva.confirmar()
        with self.assertRaises(CalculoInvalidoError):
            self.reserva.procesar(descuento=101)
        self.assertEqual(self.reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertIsNone(self.reserva.total)

    def test_no_confirmar_dos_veces(self):
        self.reserva.confirmar()
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()


class PruebasGestor(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorSoftwareFJ()
        self.gestor.agregar_cliente(Cliente("C001", "Ana", "ana@ejemplo.com", "3001234567"))
        self.gestor.agregar_servicio(ReservaSala("S001", "Sala", 50000, 20))

    def test_gestor_registros_en_listas(self):
        self.assertIsInstance(self.gestor.clientes, tuple)
        self.assertEqual(len(self.gestor.clientes), 1)

    def test_gestor_cliente_duplicado(self):
        with self.assertRaises(EntidadDuplicadaError):
            self.gestor.agregar_cliente(Cliente("C001", "Luz", "luz@ejemplo.com", "3011234567"))

    def test_gestor_reserva_inexistente(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.confirmar_reserva("R999")

    def test_no_almacena_reserva_invalida(self):
        with self.assertRaises(DatoInvalidoError):
            self.gestor.crear_reserva("R001", "C001", "S001", 0)
        self.assertEqual(len(self.gestor.reservas), 0)

    def test_flujo_gestor(self):
        self.gestor.crear_reserva("R001", "C001", "S001", 3)
        self.gestor.confirmar_reserva("R001")
        total = self.gestor.procesar_reserva("R001")
        self.assertEqual(total, Decimal("150000.00"))

    def test_no_repite_id_reserva(self):
        self.gestor.crear_reserva("R001", "C001", "S001", 2)
        with self.assertRaises(EntidadDuplicadaError):
            self.gestor.crear_reserva("R001", "C001", "S001", 1)


class PruebaDemostracion(unittest.TestCase):
    def test_demostracion_24_operaciones(self):
        resultados = simular()
        self.assertEqual(len(resultados), 24)
        self.assertTrue(all(r.aprobado for r in resultados))
        self.assertGreaterEqual(sum(r.esperado == "ERROR CONTROLADO" for r in resultados), 6)


if __name__ == "__main__":
    unittest.main()
