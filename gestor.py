
import logging
import os

from excepciones import (
    ErrorSistema,          # CAMBIO: Se importa la clase base de excepciones del sistema
    DatosInvalidosError,   # CAMBIO: Se importa para unificar errores de datos duplicados
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
        # CAMBIO: Se encapsulan las listas como atributos privados para evitar alteraciones externas directas
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        logging.info("Sistema Software FJ iniciado.")

    # CAMBIO: Se exponen propiedades de solo lectura devolviendo copias de las listas
    @property
    def clientes(self):
        return list(self.__clientes)

    @property
    def servicios(self):
        return list(self.__servicios)

    @property
    def reservas(self):
        return list(self.__reservas)

    def registrar_cliente(self, cliente):
        if any(c.identificacion == cliente.identificacion for c in self.__clientes):
            # CAMBIO: Se lanza DatosInvalidosError en lugar de ValueError para mantener la jerarquía del sistema
            raise DatosInvalidosError("El cliente ya está registrado.")

        self.__clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.nombre)

    def agregar_servicio(self, servicio):
        if any(s.codigo == servicio.codigo for s in self.__servicios):
            # CAMBIO: Se lanza DatosInvalidosError en lugar de ValueError para mantener la jerarquía del sistema
            raise DatosInvalidosError("El código del servicio ya existe.")

        self.__servicios.append(servicio)
        logging.info("Servicio agregado: %s", servicio.nombre)

    def buscar_cliente(self, identificacion):
        for cliente in self.__clientes:
            # CAMBIO: Se aplica .strip() al parámetro identificacion antes de comparar
            if cliente.identificacion == str(identificacion).strip():
                return cliente

        raise ClienteNoEncontradoError(
            f"No existe el cliente {identificacion}."
        )

    def buscar_servicio(self, codigo):
        for servicio in self.__servicios:
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
            self.__reservas.append(reserva)

            logging.info("Reserva creada: %s", reserva.codigo)

            return reserva

        # CAMBIO: Se captura ErrorSistema en lugar de Exception genérica para no ocultar fallos internos de programación
        except ErrorSistema as error:
            logging.exception("Error creando reserva.")

            raise ReservaInvalidaError(
                "No fue posible crear la reserva."
            ) from error

    def consultar_reservas(self):
        # CAMBIO: Se agrega mensaje informativo cuando aún no hay reservas registradas
        if not self.__reservas:
            print("No hay reservas registradas.")
            return

        for reserva in self.__reservas:
            print(reserva.describir())

    def registrar_evento(self, mensaje):
        logging.info(mensaje)
