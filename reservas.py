
from enum import Enum
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:

    contador = 0

    def __init__(self, cliente, servicio, duracion):
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Cliente y servicio son obligatorios.")

        servicio.validar_parametros(duracion)

        if not servicio.disponible:
            raise ReservaInvalidaError("El servicio no está disponible.")

        Reserva.contador += 1
        self.__codigo = Reserva.contador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = EstadoReserva.PENDIENTE
        self.__total = None

    @property
    def codigo(self):
        return self.__codigo

    @property
    def estado(self):
        return self.__estado

    @property
    def total(self):
        return self.__total

    def confirmar(self):
        if self.__estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = EstadoReserva.CONFIRMADA

    def cancelar(self):
        if self.__estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA
        ):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada o cancelada."
            )

        self.__estado = EstadoReserva.CANCELADA

    def procesar(self, descuento=0):
        if self.__estado != EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada."
            )

        self.__total = self.__servicio.calcular_costo(
            self.__duracion,
            descuento=descuento
        )

        self.__estado = EstadoReserva.PROCESADA
        return self.__total

    def describir(self):
        # CAMBIO: Se muestra el total formateado en moneda o un texto claro en lugar de 'None'
        total_texto = (
            f"${self.__total:,.2f}"
            if self.__total is not None
            else "Pendiente de cálculo"
        )
        return (
            f"Reserva #{self.codigo} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} | "
            f"Estado: {self.__estado.value} | "
            f"Total: {total_texto}"
        )
