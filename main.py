
from clientes import Cliente
from servicios import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from gestor import GestorSistema
# CAMBIO: Se eliminaron DatosInvalidosError y ReservaInvalidaError porque no se usaban directamente aquí
from excepciones import (
    OperacionNoPermitidaError,
    ServicioNoDisponibleError
)


def ejecutar_operacion(numero, descripcion, funcion):
    print(f"\nOPERACION {numero}: {descripcion}")

    try:
        funcion()

    except Exception as error:
        print(f"ERROR CONTROLADO: {error}")
        sistema.registrar_evento(
            f"Operación {numero} fallida: {error}"
        )

    else:
        print("Operación ejecutada correctamente.")

    finally:
        print(f"Finalizando operación {numero}.")


def operacion_1():
    cliente = Cliente(
        "1001",
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3001234567"
    )

    sistema.registrar_cliente(cliente)
    print(cliente.describir())


def operacion_2():
    cliente = Cliente(
        "1002",
        "Ana Torres",
        "correo_invalido",
        "3001234567"
    )

    sistema.registrar_cliente(cliente)


def operacion_3():
    cliente = Cliente(
        "1003",
        "Laura Gomez",
        "laura@gmail.com",
        "3101234567"
    )

    sistema.registrar_cliente(cliente)
    print(cliente.describir())


def operacion_4():
    sala = ReservaSalas(
        "S001",
        50000,
        20
    )

    sistema.agregar_servicio(sala)
    print(sala.describir())


def operacion_5():
    equipo = AlquilerEquipos(
        "E001",
        80000,
        "Computador portatil"
    )

    sistema.agregar_servicio(equipo)
    print(equipo.describir())


def operacion_6():
    asesoria = AsesoriaEspecializada(
        "A001",
        100000,
        "Desarrollo de software"
    )

    sistema.agregar_servicio(asesoria)
    print(asesoria.describir())


def operacion_7():
    reserva = sistema.crear_reserva(
        "1001",
        "S001",
        3
    )

    reserva.confirmar()

    print("Reserva confirmada:")
    print(reserva.describir())


def operacion_8():
    reserva = sistema.crear_reserva(
        "9999",
        "S001",
        2
    )

    print(reserva.describir())


def operacion_9():
    reserva = sistema.reservas[0]

    total = reserva.procesar(descuento=0.10)

    print("Reserva procesada correctamente.")
    # CAMBIO: Se formatea el valor con separador de miles y dos decimales (:,.2f)
    print(f"Total con descuento e impuestos: ${total:,.2f}")


def operacion_10():
    reserva = sistema.reservas[0]

    try:
        reserva.confirmar()

    except OperacionNoPermitidaError as error:
        print("Excepción detectada:", error)
        sistema.registrar_evento(
            f"Intento de confirmar reserva procesada: {error}"
        )


def operacion_11():
    sala = sistema.buscar_servicio("S001")

    sala.cambiar_disponibilidad(False)

    try:
        sala.calcular_costo(2)

    except ServicioNoDisponibleError as error:
        print("Servicio no disponible:", error)
        sistema.registrar_evento(str(error))


def operacion_12():
    try:
        sala = sistema.buscar_servicio("S001")
        sala.cambiar_disponibilidad(True)

        resultado = sala.calcular_costo(
            2,
            impuesto=0.19,
            descuento=0.15
        )

    except Exception as error:
        print("Error en el cálculo:", error)

    else:
        print("Cálculo realizado correctamente.")
        # CAMBIO: Se formatea el valor con separador de miles y dos decimales (:,.2f)
        print(f"Costo final: ${resultado:,.2f}")

    finally:
        print("Proceso de cálculo finalizado.")


def operacion_13():
    reserva = sistema.crear_reserva(
        "1003",
        "E001",
        2
    )

    reserva.confirmar()
    reserva.cancelar()

    print("Reserva cancelada correctamente.")
    print(reserva.describir())


if __name__ == "__main__":

    sistema = GestorSistema()

    print("=" * 55)
    print("       SISTEMA DE GESTION EMPRESARIAL")
    print("                  SOFTWARE FJ")
    print("=" * 55)

    operaciones = [
        ("Registro válido de cliente", operacion_1),
        ("Registro inválido de cliente", operacion_2),
        ("Registro de segundo cliente", operacion_3),
        ("Creación de reserva de sala", operacion_4),
        ("Creación de alquiler de equipos", operacion_5),
        ("Creación de asesoría especializada", operacion_6),
        ("Creación y confirmación de reserva", operacion_7),
        ("Reserva con cliente inexistente", operacion_8),
        ("Procesamiento y cálculo de reserva", operacion_9),
        ("Intento de confirmar reserva procesada", operacion_10),
        ("Intento de utilizar servicio no disponible", operacion_11),
        ("Cálculo con descuento e impuestos", operacion_12),
        ("Creación y cancelación de reserva", operacion_13)
    ]

    for numero, (descripcion, funcion) in enumerate(
        operaciones, start=1
    ):
        ejecutar_operacion(numero, descripcion, funcion)

    print("\n" + "=" * 55)
    print("       RESUMEN DE RESERVAS")
    print("=" * 55)

    sistema.consultar_reservas()

    print("\n" + "=" * 55)
    print("SISTEMA SOFTWARE FJ FINALIZADO.")
    print("Los eventos y errores están registrados en logs/sistema.log")
    print("=" * 55)
