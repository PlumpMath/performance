"""
Benchmark for Twisted Spread.
"""
from __future__ import division, with_statement, print_function, absolute_import

from twisted.spread.pb import PBServerFactory, PBClientFactory, Root

from performance.benchmarks.bench_twisted.benchlib import Client, driver, rotate_local_intf


class BenchRoot(Root):

    def remote_discard(self, argument):
        pass


class Client(Client):
    _structure = [
        'hello' * 100,
        {'foo': 'bar',
         'baz': 100,
         u'these are bytes': (1, 2, 3)}]

    def __init__(self, reactor, host, port):
        super(Client, self).__init__(reactor)
        self._host = host
        self._port = port

    def run(self, *args, **kwargs):
        def connected(reference):
            self._reference = reference
            return super(Client, self).run(*args, **kwargs)
        client = PBClientFactory()
        d = client.getRootObject()
        d.addCallback(connected)
        self._reactor.connectTCP(self._host, self._port, client)
        return d

    def _request(self):
        d = self._reference.callRemote('discard', self._structure)
        d.addCallback(self._continue)
        d.addErrback(self._stop)


def main(reactor, duration):
    concurrency = 15

    server = PBServerFactory(BenchRoot())
    port = reactor.listenTCP(0, server,
                             interface=rotate_local_intf())
    client = Client(reactor, port.getHost().host, port.getHost().port)
    d = client.run(concurrency, duration)
    return d


if __name__ == '__main__':
    import sys
    driver(main, sys.argv)
