"""
Módulo encargado de registrar eventos y excepciones en un archivo de texto plano.
"""

from datetime import datetime
import traceback


class RegistradorLogs:
    #Gestiona la persistencia de logs en disco de forma segura.

    def __init__(self, ruta_archivo: str = "sistema_fj.log"):
        self._ruta_archivo = ruta_archivo

    def registrar_evento(self, nivel: str, mensaje: str) -> None:
        #Escribe una línea formateada con marca de tiempo en el archivo de logs.
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        try:
            # Apertura en modo 'append' con codificación UTF-8
            with open(self._ruta_archivo, mode="a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error_io:
            # Si falla el disco, se informa por consola sin colapsar el sistema
            print(f"Fallo crítico al escribir en el log: {error_io}")

    def registrar_excepcion(self, contexto: str, excepcion: Exception) -> None:
        #Registra el detalle de una excepción y su causa encadenada si existe
        detalle_causa = ""
        if excepcion.__cause__ is not None:
            detalle_causa = f" | Causa original: {repr(excepcion.__cause__)}"

        mensaje_completo = f"Contexto: {contexto} -> {repr(excepcion)}{detalle_causa}"
        self.registrar_evento("ERROR", mensaje_completo)
