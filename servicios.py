
from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)


class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa):
        # CAMBIO: Se valida que código y nombre no sean cadenas vacías o de solo espacios
        if not codigo or not str(codigo).strip() or not nombre or not str(nombre).strip():
            raise DatosInvalidosError("Código y nombre son obligatorios.")

        # CAMBIO: Se bloquean valores booleanos (isinstance(True, int) es True en Python) antes de validar tipo numérico
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser un número positivo.")

        # CAMBIO: Se limpian espacios en código y nombre
        self._codigo = str(codigo).strip()
        self._nombre = str(nombre).strip()
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

        # CAMBIO: Se centraliza aquí la llamada a validar_parametros() para no repetir calcular_costo() en las clases hijas
        self.validar_parametros(cantidad)

        # CAMBIO: Se valida que impuesto y descuento no sean booleanos y sean numéricos dentro del rango [0, 1]
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise DatosInvalidosError("Impuesto inválido.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
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

        # CAMBIO: Se evita que un valor booleano pase como entero en capacidad
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("Capacidad inválida.")

        self.capacidad = capacidad

    def validar_parametros(self, cantidad):
        # CAMBIO: Se evita que un valor booleano pase como entero en cantidad
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Las horas deben ser un entero positivo.")

    # CAMBIO: Se eliminó el método calcular_costo() duplicado porque ahora la clase padre llama a validar_parametros()

    def describir(self):
        # CAMBIO: Se formatea la tarifa con separador de miles y dos decimales (:,.2f)
        return f"Sala | Capacidad: {self.capacidad} personas | Tarifa por hora: ${self._tarifa:,.2f}"


class AlquilerEquipos(Servicio):

    def __init__(self, codigo, tarifa, tipo_equipo):
        super().__init__(codigo, "Alquiler de equipos", tarifa)

        # CAMBIO: Se valida que tipo_equipo sea str y no tenga solo espacios
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError("Debe especificar el tipo de equipo.")

        self.tipo_equipo = tipo_equipo.strip()  # CAMBIO: Se limpia con .strip()

    def validar_parametros(self, cantidad):
        # CAMBIO: Se evita que un valor booleano pase como entero en cantidad
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Los días deben ser un entero positivo.")

    # CAMBIO: Se eliminó el método calcular_costo() duplicado porque ahora la clase padre llama a validar_parametros()

    def describir(self):
        # CAMBIO: Se formatea la tarifa con separador de miles y dos decimales (:,.2f)
        return f"Equipo: {self.tipo_equipo} | Tarifa diaria: ${self._tarifa:,.2f}"


class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, tarifa, especialidad):
        super().__init__(codigo, "Asesoría especializada", tarifa)

        # CAMBIO: Se valida que especialidad sea str y no tenga solo espacios
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Debe indicar la especialidad.")

        self.especialidad = especialidad.strip()  # CAMBIO: Se limpia con .strip()

    def validar_parametros(self, cantidad):
        # CAMBIO: Se evita que un valor booleano pase como entero en cantidad
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser un entero positivo.")

    # CAMBIO: Se eliminó el método calcular_costo() duplicado porque ahora la clase padre llama a validar_parametros()

    def describir(self):
        # CAMBIO: Se formatea la tarifa con separador de miles y dos decimales (:,.2f)
        return f"Asesoría: {self.especialidad} | Tarifa por hora: ${self._tarifa:,.2f}"
