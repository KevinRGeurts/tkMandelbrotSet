"""
Defines custom exceptions for the tkMandelbrotSet package.

Exported Classes:
    None

Exported Exceptions:
    MandelbrotSetError - Base exception class for all custom exceptions specific to tkMandelbrotSet package.
    MandelbrotSetNoPreviousZoomLocation - Custom exception to be raised when there is no previous zoom location to back up to.

Exported Functions:
    None

Logging:
    None
 """


class MandelbrotSetError(Exception):
    """
    Base exception class for all custom exceptions specific to tkMandelbrotSet package.
    """
    pass


class MandelbrotSetNoPreviousZoomLocation(MandelbrotSetError):
    """
    Custom exception to be raised when there is no previous zoom location to back up to.
    Arguments expected in **kwargs: none currently
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        # self.X_info = kwargs.get('X_info')

class MandelbrotSetNoNextZoomLocation(MandelbrotSetError):
    """
    Custom exception to be raised when there is no next zoom location to move forward to.
    Arguments expected in **kwargs: none currently
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        # self.X_info = kwargs.get('X_info')
