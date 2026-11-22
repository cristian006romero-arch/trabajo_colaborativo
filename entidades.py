
from abc import ABC, abstractmethod


class Entidad(ABC):

    def __init__(self, identificacion):
        if not identificacion:
            raise ValueError("La identificación es obligatoria.")

        self.__identificacion = str(identificacion)

    @property
    def identificacion(self):
        return self.__identificacion

    @abstractmethod
    def describir(self):
        pass
