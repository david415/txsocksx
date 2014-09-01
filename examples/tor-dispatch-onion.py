from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import clientFromString
from twisted.web import server, resource
from twisted.internet.endpoints import serverFromString

import txtorcon
import txsocksx

class GETSlash(Protocol):
    def connectionMade(self):
        self.transport.write("GET / HTTP/1.1\r\nHost: timaq4ygg2iegci7.onion\r\n\r\n")

    def buildProtocol(self):
        return self

    def dataReceived(self, data):
        print "Got this as a response"
        print data

class GETSlashFactory(Factory):
    def buildProtocol(self, addr):
        print "Building protocol towards"
        return GETSlash()


class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return "<html>Hello, world! I'm a hidden service!</html>"

site = server.Site(Simple())

def setup_failed(arg):
    print "SETUP FAILED", arg


def setup_complete(listeningPort):
    print "Received an IListeningPort %s" % (listeningPort,)
    print "..whose `getHost` gives us a %s" % listeningPort.getHost()

    address = listeningPort.getHost()
    host = address.host
    port = address.port

    def try_connect():
        print "try_connect %s %s" % (host, port)
        torEndpoint = clientFromString(reactor, "tor:host=%s:port=%s" % (host, port))
        d = torEndpoint.connect(GETSlashFactory())
        return d

    def retry_connect(failure):
        print "retry_connect"
        failure.trap(txsocksx.errors.HostUnreachable)
        return try_connect().addErrback(retry_connect)

    try_connect().addErrback(retry_connect)


hs_endpoint = serverFromString(reactor, "onion:80")
d = hs_endpoint.listen(site)
d.addCallbacks(setup_complete, setup_failed)

reactor.run()
