"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Implementa una jerarquía basada en una excepción raíz del dominio.
"""


class ErrorSistemaFJ(Exception):
    #Excepción base para todos los errores controlados de Software FJ.

    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    #Se lanza cuando un parámetro tiene formato, tipo o rango incorrecto.

    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_DATO_INVALIDO")


class ParametroFaltanteError(ErrorSistemaFJ):
    #Se lanza cuando faltan datos obligatorios para instanciar u operar

    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_PARAMETRO_FALTANTE")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    #Se lanza cuando se intenta reservar un servicio inactivo u ocupado

    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_SERVICIO_NO_DISPONIBLE")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    #Se lanza ante transiciones de estado inválidas (ej. cancelar ya cancelada).

    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_OPERACION_NO_PERMITIDA")


class CalculoInconsistenteError(ErrorSistemaFJ):
    #Se lanza cuando una operación financiera arroja valores negativos o ilógicos.

    def __init__(self, mensaje: str):
        super().__init__(mensaje, "ERR_CALCULO_INCONSISTENTE")
