from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError  # CAMBIO: Se importa la excepción personalizada del sistema


class Entidad(ABC):

    def __init__(self, identificacion):
        # CAMBIO: Se valida que no sea None ni solo espacios en blanco, y se lanza DatosInvalidosError en lugar de ValueError
        if identificacion is None or not str(identificacion).strip():
            raise DatosInvalidosError("La identificación es obligatoria.")

        # CAMBIO: Se limpia con .strip() para evitar espacios accidentales al inicio o final
        self.__identificacion = str(identificacion).strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @abstractmethod
    def describir(self):
        pass
