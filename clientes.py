
import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener mínimo 3 caracteres.")

        if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", correo):
            raise DatosInvalidosError("El correo electrónico no es válido.")

        if not str(telefono).isdigit() or len(str(telefono)) < 7:
            raise DatosInvalidosError("El teléfono debe tener mínimo 7 dígitos.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = str(telefono)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def describir(self):
        return (
            f"Cliente: {self.nombre} | "
            f"ID: {self.identificacion} | "
            f"Correo: {self.correo}"
        )
