"""
This benchmark runs a trivial Twisted Web server and client and makes as many
requests as it can in a fixed period of time.

A significant problem with this benchmark is the lack of persistent connections
in the HTTP client.  Lots of TCP connections means lots of overhead in the
kernel that's not really what we're trying to benchmark.  Plus lots of sockets
end up in TIME_WAIT which has a (briefly) persistent effect on system-wide
performance and makes consecutive runs of the benchmark vary wildly in their
results.
"""
from __future__ import division, with_statement, print_function, absolute_import

from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.web.server import Site
from twisted.web.static import Data
from twisted.web.resource import Resource
from twisted.web.client import ResponseDone, Agent

from performance.benchmarks.bench_twisted.benchlib import Client, driver


class BodyConsumer(Protocol):

    def __init__(self, finished):
        self.finished = finished

    def connectionLost(self, reason):
        if reason.check(ResponseDone):
            self.finished.callback(None)
        else:
            self.finished.errback(reason)


class Client(Client):

    def __init__(self, reactor, host, portNumber, agent):
        self._requestLocation = 'http://%s:%d/' % (host, portNumber,)
        self._agent = agent
        super(Client, self).__init__(reactor)

    def _request(self):
        d = self._agent.request('GET', self._requestLocation)
        d.addCallback(self._read)
        d.addCallback(self._continue)
        d.addErrback(self._stop)

    def _read(self, response):
        finished = Deferred()
        response.deliverBody(BodyConsumer(finished))
        return finished


def main(reactor, duration):
    interfaceCounter = int(reactor.seconds()) % 254 + 1

    interface = '127.0.0.%d' % (interfaceCounter,)

    concurrency = 10

    class BindLocalReactor(object):

        def __init__(self, reactor):
            self._reactor = reactor

        def __getattr__(self, name):
            return getattr(self._reactor, name)

        def connectTCP(self, host, port, factory, timeout=30, bindAddress=(interface, 0)):
            return self._reactor.connectTCP(host, port, factory, timeout, bindAddress)

    root = Resource()
    root.putChild('', Data("Hello, world", "text/plain"))

    port = reactor.listenTCP(
        0, Site(root), backlog=128, interface=interface)
    agent = Agent(BindLocalReactor(reactor))
    client = Client(reactor, port.getHost().host, port.getHost().port, agent)
    d = client.run(concurrency, duration)

    def cleanup(passthrough):
        d = port.stopListening()
        d.addCallback(lambda ignored: passthrough)
        return d
    d.addBoth(cleanup)
    return d


if __name__ == '__main__':
    import sys
    driver(main, sys.argv)
