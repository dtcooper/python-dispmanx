class DispmanXRuntimeError(RuntimeError):
    """Raised when an **irrecoverable** error occurs with the underlying DispmanX library.

    Under normal circumstances, you should destroy any [DispmanX][dispmanx.DispmanX]
    objects you've instantiated when one of these exceptions gets raises. Or,
    your program should cleanly exit.
    """

    pass


class DispmanXError(Exception):
    """Raised when a **recoverable** error occurs with the underlying DispmanX library.

    Likely a programmer error. You can try whatever you were doing again and
    correcting the offending behavior."""

    pass
