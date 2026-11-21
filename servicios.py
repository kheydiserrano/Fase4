"""
Módulo con las implementaciones concretas de los servicios de Software FJ.
Demuestra herencia, polimorfismo y sobrescritura de métodos.
"""

from modelos_base import Servicio
from excepciones import DatoInvalidoError, CalculoInconsistenteError


class ReservaSala(Servicio):
    #Servicio especializado para reserva de salas fisicas o de conferencias.

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad_maxima: int):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatoInvalidoError("La capacidad máxima de la sala debe ser un entero positivo.")
        self._capacidad_maxima = capacidad_maxima

    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima

    def validar_parametros_operacion(self, duracion: int, **parametros_extra) -> None:
        asistentes = parametros_extra.get("asistentes", 1)
        if not isinstance(duracion, int) or duracion < 1 or duracion > 12:
            raise DatoInvalidoError("La reserva de sala debe durar entre 1 y 12 horas.")
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise DatoInvalidoError("El número de asistentes debe ser mayor a cero.")
        if asistentes > self._capacidad_maxima:
            raise DatoInvalidoError(
                f"Los asistentes ({asistentes}) superan la capacidad máxima de la sala ({self._capacidad_maxima})."
            )

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        **parametros_extra
    ) -> float:
        self.validar_parametros_operacion(duracion, **parametros_extra)
        catering = bool(parametros_extra.get("incluir_catering", False))

        subtotal = self.tarifa_base * duracion
        if catering:
            asistentes = parametros_extra.get("asistentes", 1)
            subtotal += asistentes * 15.0  # Cargo fijo por refrigerio por asistente

        total = (subtotal * (1 - descuento)) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo de costo de sala arrojó un valor no positivo.")
        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return (
            f"Sala [{self.id}] '{self.nombre}' | Capacidad: {self._capacidad_maxima} pers. | "
            f"Tarifa: ${self.tarifa_base}/h | Estado: {estado}"
        )


class AlquilerEquipo(Servicio):
    #Servicio especializado para alquiler de hardware y equipamiento tecnológico.

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, deposito_garantia: float):
        super().__init__(id_servicio, nombre, tarifa_dia)
        if deposito_garantia < 0:
            raise DatoInvalidoError("El depósito de garantía no puede ser negativo.")
        self._deposito_garantia = float(deposito_garantia)

    def validar_parametros_operacion(self, duracion: int, **parametros_extra) -> None:
        cantidad = parametros_extra.get("cantidad", 1)
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise DatoInvalidoError("El alquiler de equipos debe ser entre 1 y 30 días.")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise DatoInvalidoError("La cantidad de equipos a alquilar debe ser al menos 1.")

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        **parametros_extra
    ) -> float:
        self.validar_parametros_operacion(duracion, **parametros_extra)
        cantidad = parametros_extra.get("cantidad", 1)

        subtotal_alquiler = (self.tarifa_base * duracion) * cantidad
        monto_gravable = subtotal_alquiler * (1 - descuento)
        # El depósito de garantía no lleva IVA
        total = (monto_gravable * (1 + impuesto)) + (self._deposito_garantia * cantidad)

        if total <= 0:
            raise CalculoInconsistenteError("El costo del alquiler resultó inconsistente.")
        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Alquilado"
        return (
            f"Equipo [{self.id}] '{self.nombre}' | Tarifa: ${self.tarifa_base}/día | "
            f"Garantía: ${self._deposito_garantia} | Estado: {estado}"
        )


class AsesoriaEspecializada(Servicio):
    #Servicio especializado de consultoría técnica o arquitectura de software.

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not especialidad or len(especialidad.strip()) < 3:
            raise DatoInvalidoError("Debe especificar una especialidad válida para la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros_operacion(self, duracion: int, **parametros_extra) -> None:
        if not isinstance(duracion, int) or duracion < 1:
            raise DatoInvalidoError("La asesoría debe durar al menos 1 hora.")

    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        **parametros_extra
    ) -> float:
        self.validar_parametros_operacion(duracion, **parametros_extra)
        urgente = bool(parametros_extra.get("urgente", False))

        subtotal = self.tarifa_base * duracion
        if urgente:
            subtotal *= 1.25  # Recargo del 25% por atención prioritaria

        total = (subtotal * (1 - descuento)) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo de la asesoría generó un monto inválido.")
        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Asesoría [{self.id}] '{self.nombre}' ({self._especialidad}) | "
            f"Tarifa: ${self.tarifa_base}/h | Estado: {estado}"
        )
