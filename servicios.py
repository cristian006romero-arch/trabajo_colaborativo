
from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)


class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa):
        if not codigo or not nombre:
            raise DatosInvalidosError("Código y nombre son obligatorios.")

        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser positiva.")

        self._codigo = codigo
        self._nombre = nombre
        self._tarifa = float(tarifa)
        self._disponible = True

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("El estado debe ser verdadero o falso.")
        self._disponible = estado

    def calcular_costo(self, cantidad=1, impuesto=0.19, descuento=0):
        if not self.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")

        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser positiva.")

        if not 0 <= impuesto <= 1:
            raise DatosInvalidosError("Impuesto inválido.")

        if not 0 <= descuento <= 1:
            raise DatosInvalidosError("Descuento inválido.")

        subtotal = self._tarifa * cantidad
        total = subtotal * (1 - descuento) * (1 + impuesto)

        if total < 0:
            raise CalculoInconsistenteError("El cálculo produjo un valor negativo.")

        return round(total, 2)

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        pass


class ReservaSalas(Servicio):

    def __init__(self, codigo, tarifa, capacidad):
        super().__init__(codigo, "Reserva de salas", tarifa)

        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("Capacidad inválida.")

        self.capacidad = capacidad

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Las horas deben ser un entero positivo.")

    def calcular_costo(self, cantidad=1, impuesto=0.19, descuento=0):
        self.validar_parametros(cantidad)
        return super().calcular_costo(cantidad, impuesto, descuento)

    def describir(self):
        return f"Sala | Capacidad: {self.capacidad} personas | Tarifa por hora: ${self._tarifa}"


class AlquilerEquipos(Servicio):

    def __init__(self, codigo, tarifa, tipo_equipo):
        super().__init__(codigo, "Alquiler de equipos", tarifa)

        if not tipo_equipo:
            raise DatosInvalidosError("Debe especificar el tipo de equipo.")

        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Los días deben ser un entero positivo.")

    def calcular_costo(self, cantidad=1, impuesto=0.19, descuento=0):
        self.validar_parametros(cantidad)
        return super().calcular_costo(cantidad, impuesto, descuento)

    def describir(self):
        return f"Equipo: {self.tipo_equipo} | Tarifa diaria: ${self._tarifa}"


class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, tarifa, especialidad):
        super().__init__(codigo, "Asesoría especializada", tarifa)

        if not especialidad:
            raise DatosInvalidosError("Debe indicar la especialidad.")

        self.especialidad = especialidad

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")

    def calcular_costo(self, cantidad=1, impuesto=0.19, descuento=0):
        self.validar_parametros(cantidad)
        return super().calcular_costo(cantidad, impuesto, descuento)

    def describir(self):
        return f"Asesoría: {self.especialidad} | Tarifa por hora: ${self._tarifa}"
