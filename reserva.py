"""
Módulo que gestiona el ciclo de vida de una Reserva en Software FJ.
"""

from modelos_base import EntidadBase, Servicio
from cliente import Cliente
from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    ErrorSistemaFJ
)


class Reserva(EntidadBase):
    #Asocia un Cliente con un Servicio durante un tiempo determinado.

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        **parametros_servicio
    ):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")
        if not (0.0 <= descuento < 1.0):
            raise DatoInvalidoError("El descuento debe estar en el rango [0.0, 1.0).")
        if impuesto < 0:
            raise DatoInvalidoError("El impuesto no puede ser negativo.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._impuesto = impuesto
        self._descuento = descuento
        self._parametros_servicio = parametros_servicio
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

        # Cálculo inicial polimórfico que además valida los parámetros del servicio
        self._costo_total = self._servicio.calcular_costo(
            self._duracion,
            impuesto=self._impuesto,
            descuento=self._descuento,
            **self._parametros_servicio
        )

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar(self) -> None:
        #Confirma la reserva y bloquea la disponibilidad del servicio.
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.id} porque su estado actual es '{self._estado}'."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' ({self._servicio.id}) no está disponible."
            )

        self._estado = "CONFIRMADA"
        self._servicio.disponible = False

    def cancelar(self) -> None:
        #Cancela una reserva activa y libera el servicio.
        if self._estado in ("CANCELADA", "COMPLETADA"):
            raise OperacionNoPermitidaError(
                f"La reserva {self.id} ya se encuentra '{self._estado}' y no puede cancelarse."
            )

        estado_anterior = self._estado
        self._estado = "CANCELADA"
        if estado_anterior == "CONFIRMADA":
            self._servicio.disponible = True

    def procesar_finalizacion(self) -> None:
        #Marca la reserva como completada y libera el recurso.
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden completar reservas confirmadas. Estado actual: '{self._estado}'."
            )
        self._estado = "COMPLETADA"
        self._servicio.disponible = True

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | Total: ${self._costo_total:.2f}"
        )
