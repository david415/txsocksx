
from twisted.plugin import IPlugin
from twisted.internet.interfaces import IStreamClientEndpointStringParser
from twisted.internet.endpoints import clientFromString
from zope.interface import implementer

from txsocksx.client import TorClientEndpoint

@implementer(IPlugin, IStreamClientEndpointStringParser)
class TorClientEndpointStringParser(object):
    prefix = "tor"

    def _parseClient(self, host=None, port=None):
        if port is not None:
            port = int(port)

        return TorClientEndpoint(host, port)

    def parseStreamClient(self, *args, **kwargs):
        return self._parseClient(*args, **kwargs)
