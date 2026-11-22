import re
from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre debe tener mínimo 3 caracteres.")

        if not isinstance(correo, str) or not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", correo.strip()):
            raise DatosInvalidosError("El correo electrónico no es válido.")

        telefono_limpio = str(telefono).strip().replace(" ", "")
        if not telefono_limpio.isdigit() or len(telefono_limpio) < 7:
            raise DatosInvalidosError("El teléfono debe tener mínimo 7 dígitos.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono_limpio

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
