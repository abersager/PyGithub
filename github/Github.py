from Requester import Requester
from GithubObjects import *

class Github:
    def __init__( self, login=None, password=None ):
        self.__requester = Requester( login=login, password=password )

    def _dataRequest( self, verb, url, parameters, data ):
        return self.__requester.dataRequest( verb, url, parameters, data )

    def _statusRequest( self, verb, url, parameters, data ):
        return self.__requester.statusRequest( verb, url, parameters, data )

    def get_user( self, login = None ):
        if login is None:
            return AuthenticatedUser( self, {}, lazy = True )
        else:
            return NamedUser( self, { "login": login }, lazy = False )

    def get_organization( self, login ):
        return Organization( self, { "login": login }, lazy = False )

    def get_gist( self, id ):
        return Gist( self, { "id": id }, lazy = False )

    def get_gists( self ):
        return [
            Gist( self, attributes, lazy = True )
            for attributes
            in self._dataRequest( "GET", "/gists/public", None, None )
        ]
