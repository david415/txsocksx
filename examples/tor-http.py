#!/usr/bin/env python

from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.interfaces import IStreamClientEndpointStringParser
from twisted.internet.endpoints import clientFromString
from twisted.internet.endpoints import TCP4ClientEndpoint

# thanks to hellais for the original code
# https://github.com/hellais/txsocksx/blob/master/examples/example.py

class GETSlash(Protocol):
    def connectionMade(self):
        self.transport.write("GET / HTTP/1.1\n\r\n\r")

    def buildProtocol(self):
        return self

    def dataReceived(self, data):
        print "Got this as a response"
        print data

class GETSlashFactory(Factory):
    def buildProtocol(self, addr):
        print "Building protocol towards"
        return GETSlash()



torEndpoint = clientFromString(reactor, "tor:host=timaq4ygg2iegci7.onion:port=80")

d = torEndpoint.connect(GETSlashFactory())
@d.addErrback
def _gotError(error):
    print error
    print "Error in connection"
    reactor.stop()

reactor.run()
