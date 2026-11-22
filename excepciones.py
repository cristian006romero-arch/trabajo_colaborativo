
class ErrorSistema(Exception):
    """Excepción general del sistema Software FJ."""
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class ClienteNoEncontradoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaInvalidaError(ErrorSistema):
    pass


class OperacionNoPermitidaError(ErrorSistema):
    pass


class CalculoInconsistenteError(ErrorSistema):
    pass
