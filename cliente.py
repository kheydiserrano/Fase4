"""
Módulo de gestión de clientes con encapsulación y validación de datos personales.
"""

import re
from modelos_base import EntidadBase
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    #Representa un cliente registrado en Software FJ.

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3 or any(char.isdigit() for char in valor):
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. No debe contener números.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, valor.strip()):
            raise DatoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El teléfono de contacto es obligatorio.")
        digitos = re.sub(r"\D", "", valor)
        if len(digitos) < 7 or len(digitos) > 15:
            raise DatoInvalidoError(f"Número telefónico inválido: '{valor}'. Debe tener entre 7 y 15 dígitos.")
        self._telefono = digitos

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}]: {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"
