"""
Punto de entrada principal del sistema de Software FJ.
Ejecuta 12 operaciones simuladas demostrando estabilidad ante errores y trazabilidad en logs.
"""

from logger import RegistradorLogs
from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSistemaFJ


def ejecutar_simulacion():
    logger = RegistradorLogs("sistema_fj.log")
    logger.registrar_evento("SYSTEM", "=== INICIO DE SIMULACIÓN SOFTWARE FJ ===")
    gestor = GestorSoftwareFJ(logger)

    print("\n--- FASE 1: REGISTRO DE CLIENTES ---")
    # Operación 1: Registro de cliente válido
    gestor.registrar_cliente("CLI-01", "Laura Mendoza", "laura.mendoza@correo.com", "3104567890")

    # Operación 2: Registro de cliente válido
    gestor.registrar_cliente("CLI-02", "Carlos Restrepo", "crestrepo@empresa.co", "3209876543")

    # Operación 3: Registro de cliente INVÁLIDO (correo mal formado y nombre con números)
    gestor.registrar_cliente("CLI-03", "Pedro123", "pedro_sin_arroba.com", "123")

    # Operación 4: Registro de cliente INVÁLIDO (ID duplicado)
    gestor.registrar_cliente("CLI-01", "Laura Duplicada", "otra@correo.com", "3001112233")

    print("\n--- FASE 2: CREACIÓN DE SERVICIOS ---")
    # Operación 5: Creación correcta de Sala
    sala_juntas = ReservaSala("SRV-S01", "Sala Ejecutiva Norte", tarifa_hora=50.0, capacidad_maxima=10)
    gestor.registrar_servicio(sala_juntas)

    # Operación 6: Creación correcta de Equipo
    servidor_portatil = AlquilerEquipo("SRV-E01", "Workstation Dell Precision", tarifa_dia=35.0, deposito_garantia=100.0)
    gestor.registrar_servicio(servidor_portatil)

    # Operación 7: Creación correcta de Asesoría
    asesoria_cloud = AsesoriaEspecializada("SRV-A01", "Arquitectura Cloud", tarifa_hora=80.0, especialidad="DevOps y AWS")
    gestor.registrar_servicio(asesoria_cloud)

    # Operación 8: Creación INCORRECTA de servicio (tarifa negativa capturada en main)
    try:
        servicio_erroneo = ReservaSala("SRV-S99", "Sala Fantasma", tarifa_hora=-20.0, capacidad_maxima=5)
        gestor.registrar_servicio(servicio_erroneo)
    except ErrorSistemaFJ as e:
        logger.registrar_excepcion("Instanciación directa de servicio", e)
        print(f"[AVISO] Error controlado al instanciar servicio: {e}")

    print("\n--- FASE 3: GESTIÓN DE RESERVAS Y SOBRECARGA DE COSTOS ---")
    # Operación 9: Reserva exitosa de Sala con parámetros extra (catering y asistentes) y descuento del 10%
    gestor.crear_y_confirmar_reserva(
        id_reserva="RES-101",
        id_cliente="CLI-01",
        id_servicio="SRV-S01",
        duracion=4,
        descuento=0.10,
        asistentes=8,
        incluir_catering=True
    )

    # Operación 10: Reserva FALLIDA porque la sala SRV-S01 ya fue confirmada y está ocupada
    gestor.crear_y_confirmar_reserva(
        id_reserva="RES-102",
        id_cliente="CLI-02",
        id_servicio="SRV-S01",
        duracion=2,
        asistentes=4
    )

    # Operación 11: Reserva exitosa de Asesoría con recargo de urgencia (parámetro opcional)
    gestor.crear_y_confirmar_reserva(
        id_reserva="RES-103",
        id_cliente="CLI-02",
        id_servicio="SRV-A01",
        duracion=3,
        impuesto=0.19,
        urgente=True
    )

    # Operación 12: Reserva FALLIDA por exceso de asistentes en sala (tras cancelar RES-101)
    gestor.cancelar_reserva("RES-101")
    gestor.crear_y_confirmar_reserva(
        id_reserva="RES-104",
        id_cliente="CLI-02",
        id_servicio="SRV-S01",
        duracion=2,
        asistentes=25  # Supera el máximo de 10
    )

    # Operación 13 (Adicional): Reserva exitosa de Alquiler de Equipos (2 unidades por 5 días)
    gestor.crear_y_confirmar_reserva(
        id_reserva="RES-105",
        id_cliente="CLI-01",
        id_servicio="SRV-E01",
        duracion=5,
        cantidad=2
    )

    logger.registrar_evento("SYSTEM", "=== FIN DE SIMULACIÓN SOFTWARE FJ (SISTEMA ESTABLE) ===")
    print("\nSimulación finalizada sin interrupciones. Revise el archivo 'sistema_fj.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()
