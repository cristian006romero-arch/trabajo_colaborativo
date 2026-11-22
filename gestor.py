
import logging
import os

from excepciones import (
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError
)
from reservas import Reserva


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True
)


class GestorSistema:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

        logging.info("Sistema Software FJ iniciado.")

    def registrar_cliente(self, cliente):
        if any(c.identificacion == cliente.identificacion for c in self.clientes):
            raise ValueError("El cliente ya está registrado.")

        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.nombre)

    def agregar_servicio(self, servicio):
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise ValueError("El código del servicio ya existe.")

        self.servicios.append(servicio)
        logging.info("Servicio agregado: %s", servicio.nombre)

    def buscar_cliente(self, identificacion):
        for cliente in self.clientes:
            if cliente.identificacion == str(identificacion):
                return cliente

        raise ClienteNoEncontradoError(
            f"No existe el cliente {identificacion}."
        )

    def buscar_servicio(self, codigo):
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                if not servicio.disponible:
                    raise ServicioNoDisponibleError(
                        "El servicio está deshabilitado."
                    )
                return servicio

        raise ServicioNoDisponibleError(
            f"No existe el servicio {codigo}."
        )

    def crear_reserva(self, identificacion, codigo_servicio, duracion):
        try:
            cliente = self.buscar_cliente(identificacion)
            servicio = self.buscar_servicio(codigo_servicio)

            reserva = Reserva(cliente, servicio, duracion)
            self.reservas.append(reserva)

            logging.info("Reserva creada: %s", reserva.codigo)

            return reserva

        except Exception as error:
            logging.exception("Error creando reserva.")

            raise ReservaInvalidaError(
                "No fue posible crear la reserva."
            ) from error

    def consultar_reservas(self):
        for reserva in self.reservas:
            print(reserva.describir())

    def registrar_evento(self, mensaje):
        logging.info(mensaje)
