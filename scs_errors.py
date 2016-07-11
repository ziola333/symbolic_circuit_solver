""" Module holds derivative of Exceptions to be properly handled. Just empty classes.
"""

__author__ = "Tomasz Kniola"
__credits__ = ["Tomasz Kniola"]

__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "kniola.tomasz@gmail.com"
__status__ = "development"

class ScsParserError(BaseException):
    """ Error which occured during parsing a file or a expresion.
    """
    None

class ScsInstanceError(BaseException):
    """ Error which occured during instantiating or solving a circuit.
    """
    None

class ScsParameterError(BaseException):
    """ Error which occured in relation with parameters.
    """
    None

class ScsElementError(BaseException):
    """ Error which occured in relation with elements.
    """
    None

class ScsAnalysisError(BaseException):
    """ Error which occured in relation with elements.
    """
    None