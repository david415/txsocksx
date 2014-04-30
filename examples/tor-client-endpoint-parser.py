#!/usr/bin/env python

from zope.interface import implementer
from twisted.plugin import IPlugin
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.interfaces import IStreamClientEndpointStringParser
from twisted.internet.endpoints import clientFromString
from twisted.internet.endpoints import TCP4ClientEndpoint

from txsocksx.client import SOCKS5ClientEndpoint


@implementer(IPlugin, IStreamClientEndpointStringParser)
class TorClientEndpointStringParser(object):
    prefix = "tor"

    def _parseClient(self, host=None, port=None):

        assert (host and port) is not None

        socks_addr = '127.0.0.1'
        socks_port = 9050
        TCPPoint   = TCP4ClientEndpoint(reactor, socks_addr, socks_port)

        socks5ClientEndpoint = SOCKS5ClientEndpoint(host, port, TCPPoint)        
        return socks5ClientEndpoint


    def parseStreamClient(self, *args, **kwargs):
        return self._parseClient(*args, **kwargs)

