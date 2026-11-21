"""
Controlador principal de Software FJ.
Administra listas internas en memoria y coordina el registro de logs.
"""

from typing import List, Optional
from cliente import Cliente
from modelos_base import Servicio
from reserva import Reserva
from logger import RegistradorLogs
from excepciones import ErrorSistemaFJ, DatoInvalidoError


class GestorSoftwareFJ:
    #Gestiona clientes, servicios y reservas en memoria sin base de datos.

    def __init__(self, logger: RegistradorLogs):
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
        self._logger = logger

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        return next((c for c in self._clientes if c.id == id_cliente), None)

    def buscar_servicio(self, id_servicio: str) -> Optional[Servicio]:
        return next((s for s in self._servicios if s.id == id_servicio), None)

    def buscar_reserva(self, id_reserva: str) -> Optional[Reserva]:
        return next((r for r in self._reservas if r.id == id_reserva), None)

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        #Crea y almacena un cliente capturando y registrando cualquier error.
        nuevo_cliente = None
        try:
            if self.buscar_cliente(id_cliente) is not None:
                raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{id_cliente}'.")
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as error:
            self._logger.registrar_excepcion(f"Registro de cliente ({id_cliente})", error)
            print(f"[AVISO] No se pudo registrar cliente {id_cliente}: {error}")
        except Exception as error_inesperado:
            # Encadenamiento de excepción inesperada hacia la jerarquía del sistema
            error_encadenado = ErrorSistemaFJ("Fallo interno al crear cliente.")
            error_encadenado.__cause__ = error_inesperado
            self._logger.registrar_excepcion(f"Registro crítico cliente ({id_cliente})", error_encadenado)
            print(f"[ERROR CRÍTICO] {error_encadenado}")
        else:
            # Solo se ejecuta si no hubo excepciones
            self._clientes.append(nuevo_cliente)
            self._logger.registrar_evento("INFO", f"Cliente registrado exitosamente: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
        finally:
            # Se ejecuta siempre para trazabilidad
            self._logger.registrar_evento("TRACE", f"Finalizado intento de alta de cliente ID={id_cliente}")

        return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> bool:
        #Agrega una instancia de Servicio (polimórfica) al catálogo.
        exito = False
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("El objeto proporcionado no es un Servicio válido.")
            if self.buscar_servicio(servicio.id) is not None:
                raise DatoInvalidoError(f"El servicio con ID '{servicio.id}' ya existe.")
        except ErrorSistemaFJ as error:
            self._logger.registrar_excepcion("Registro de servicio", error)
            print(f"[AVISO] Error al registrar servicio: {error}")
        else:
            self._servicios.append(servicio)
            self._logger.registrar_evento("INFO", f"Servicio añadido: {servicio.obtener_resumen()}")
            print(f"[OK] {servicio.obtener_resumen()}")
            exito = True
        finally:
            self._logger.registrar_evento("TRACE", "Operación de registro de servicio concluida.")

        return exito

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        confirmar_inmediato: bool = True,
        **parametros_extra
    ) -> Optional[Reserva]:
        #Orquesta la creación y confirmación opcional de una reserva.
        reserva = None
        try:
            if self.buscar_reserva(id_reserva) is not None:
                raise DatoInvalidoError(f"El ID de reserva '{id_reserva}' ya está en uso.")

            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise DatoInvalidoError(f"No existe ningún cliente con ID '{id_cliente}'.")

            servicio = self.buscar_servicio(id_servicio)
            if servicio is None:
                raise DatoInvalidoError(f"No existe ningún servicio con ID '{id_servicio}'.")

            reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
                impuesto=impuesto,
                descuento=descuento,
                **parametros_extra
            )

            if confirmar_inmediato:
                reserva.confirmar()

        except ErrorSistemaFJ as error:
            self._logger.registrar_excepcion(f"Creación de reserva ({id_reserva})", error)
            print(f"[AVISO] Fallo en reserva {id_reserva}: {error}")
            reserva = None
        except Exception as error_general:
            try:
                raise ErrorSistemaFJ(f"Error inesperado procesando reserva {id_reserva}") from error_general
            except ErrorSistemaFJ as encadenada:
                self._logger.registrar_excepcion(f"Reserva ({id_reserva})", encadenada)
                print(f"[ERROR CRÍTICO] {encadenada}")
                reserva = None
        else:
            self._reservas.append(reserva)
            self._logger.registrar_evento("INFO", f"Reserva procesada: {reserva.obtener_resumen()}")
            print(f"[OK] {reserva.obtener_resumen()}")
        finally:
            self._logger.registrar_evento("TRACE", f"Cierre de transacción reserva ID={id_reserva}")

        return reserva

    def cancelar_reserva(self, id_reserva: str) -> None:
        #Gestiona la cancelación controlada de una reserva existente.
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise DatoInvalidoError(f"No se encontró la reserva '{id_reserva}'.")
            reserva.cancelar()
        except ErrorSistemaFJ as error:
            self._logger.registrar_excepcion(f"Cancelación reserva ({id_reserva})", error)
            print(f"[AVISO] No se pudo cancelar {id_reserva}: {error}")
        else:
            self._logger.registrar_evento("INFO", f"Reserva cancelada: {id_reserva}")
            print(f"[OK] Reserva {id_reserva} cancelada correctamente.")
