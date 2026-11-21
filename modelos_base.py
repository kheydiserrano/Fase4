"""
Módulo que define las clases abstractas fundamentales de la arquitectura.
"""

from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    #Clase abstracta raíz que representa cualquier entidad identificable del sistema.

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        self._id = id_entidad.strip()

    @property
    def id(self) -> str:
        #Retorna el identificador único encapsulado.
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        #Método abstracto que obliga a las subclases a describir su estado.
        pass


class Servicio(EntidadBase, ABC):
    """
    Clase abstracta que modela un servicio ofrecido por Software FJ.
    Hereda de EntidadBase e impone contratos polimórficos.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            tarifa = float(valor)
        except (TypeError, ValueError) as e:
            # Encadenamiento de excepciones ante tipos no numéricos
            raise DatoInvalidoError("La tarifa base debe ser un valor numérico.") from e

        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")
        self._tarifa_base = tarifa

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise DatoInvalidoError("La disponibilidad debe ser un valor booleano.")
        self._disponible = estado

    @abstractmethod
    def validar_parametros_operacion(self, duracion: int, **parametros_extra) -> None:
        #Valida reglas de negocio específicas de cada tipo de servicio.
        pass

    @abstractmethod
    def calcular_costo(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        **parametros_extra
    ) -> float:
        """
        Calcula el costo total del servicio.
        Soporta sobrecarga funcional mediante parámetros opcionales y kwargs.
        """
        pass
