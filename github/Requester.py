import httplib
import json
import base64
import urllib

class UnknownGithubObject( Exception ):
    pass

class Requester:
    def __init__( self, login=None, password=None ):
        if login is not None and password is not None:
            self.__authorizationHeader = "Basic " + base64.b64encode(
                login + ":" + password ).replace( '\n', '' )

    def dataRequest( self, verb, url, parameters, input ):
        if parameters is None:
            parameters = dict()

        headers, output = self.__statusCheckedRequest( verb, url, parameters, input )

        obviouslyFinished = False
        pageCount = 1
        while "link" in headers and "next" in headers[ "link" ] and not obviouslyFinished and pageCount < 10:
            for link in headers[ "link" ].split( "," ):
                if "next" in link:
                    linkUrl = link.split( ";" )[ 0 ][ : -1 ]
                    params = linkUrl.split( "?" )[ 1 ]
                    parameters.update( dict( p.split( "=" ) for p in params.split( "&" ) ) )
                    break
            headers, newOutput = self.__statusCheckedRequest( verb, url, parameters, input )
            pageCount += 1
            if len( newOutput ) == 0:
                obviouslyFinished = True
            output += newOutput

        return output

    def __statusCheckedRequest( self, verb, url, parameters, input ):
        status, headers, output = self.__rawRequest( verb, url, parameters, input )
        if status < 200 or status >= 300:
            raise UnknownGithubObject()
        return headers, output

    def statusRequest( self, verb, url, parameters, input ):
        status, headers, output = self.__rawRequest( verb, url, parameters, input )
        return status

    def __rawRequest( self, verb, url, parameters, input ):
        assert verb in [ "HEAD", "GET", "POST", "PATCH", "PUT", "DELETE" ]

        cnx = httplib.HTTPSConnection( "api.github.com", strict = True )
        params = {}
        if hasattr(self, '__authorizationHeader'):
            params.update({ "Authorization" : self.__authorizationHeader })
        cnx.request(
            verb,
            self.__completeUrl( url, parameters ),
            json.dumps( input ),
            params
        )
        response = cnx.getresponse()

        status = response.status
        headers = dict( response.getheaders() )
        output = self.__strucutredFromJson( response.read() )

        cnx.close()

        # print verb, url, parameters, input, "==>", status, str( headers )[ :30 ], str( output )[ :30 ]
        return status, headers, output

    def __completeUrl( self, url, parameters ):
        if parameters is None or len( parameters ) == 0:
            return url
        else:
            return url + "?" + urllib.urlencode( parameters )

    def __strucutredFromJson( self, data ):
        if len( data ) == 0:
            return None
        else:
            return json.loads( data )
