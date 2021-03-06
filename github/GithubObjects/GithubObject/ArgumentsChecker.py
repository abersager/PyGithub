import itertools

class Parameters:
    def __init__( self, mandatoryParameters, optionalParameters ):
        self.__mandatoryParameters = mandatoryParameters
        self.__optionalParameters = optionalParameters

    def check( self, args, kwds ):
        data = dict( kwds )
        for arg, argumentName in itertools.izip( args, itertools.chain( self.__mandatoryParameters, self.__optionalParameters ) ):
            if argumentName in kwds:
                raise TypeError()
            else:
                data[ argumentName ] = arg
        for argumentName in data:
            if argumentName not in itertools.chain( self.__mandatoryParameters, self.__optionalParameters ):
                raise TypeError()
        for argumentName in self.__mandatoryParameters:
            if argumentName not in data:
                raise TypeError()
        return data

    def documentParameters( self ):
        mandatory = ", ".join( self.__mandatoryParameters )
        optional = "[" + ", ".join( self.__optionalParameters ) + "]"

        if len( self.__mandatoryParameters ) == 0:
            if len( self.__optionalParameters ) == 0:
                return ""
            else:
                return " " + optional + " "
        else:
            if len( self.__optionalParameters ) == 0:
                return " " + mandatory + " "
            else:
                return " " + mandatory + ", " + optional + " "

def NoParameters():
    return Parameters( [], [] )

class Alternative:
    def __init__( self, *checkers ):
        self.__checkers = checkers

    def check( self, args, kwds ):
        # Try the n - 1 first checkers
        for checker in self.__checkers[ : -1 ]:
            try:
                return checker.check( args, kwds )
            except TypeError:
                pass
        # Use the last checker
        # This way, the call stack will point to an actual validation failure
        return self.__checkers[ -1 ].check( args, kwds )

    def documentParameters( self ):
        return " <" + "> or <".join( checker.documentParameters() for checker in self.__checkers ) + "> "
