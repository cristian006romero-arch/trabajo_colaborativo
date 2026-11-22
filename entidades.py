from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class Entidad(ABC):

    def __init__(self, identificacion):
        if identificacion is None or not str(identificacion).strip():
            raise DatosInvalidosError("La identificación es obligatoria.")

        self.__identificacion = str(identificacion).strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @abstractmethod
    def describir(self):
        pass
