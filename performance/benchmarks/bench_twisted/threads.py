from __future__ import division, with_statement, print_function, absolute_import

from twisted.internet.threads import deferToThread

from performance.benchmarks.bench_twisted.benchlib import Client, driver


class Client(Client):

    def _request(self):
        d = deferToThread(lambda: None)
        d.addCallback(self._continue)
        d.addErrback(self._stop)


def main(reactor, duration):
    concurrency = 10

    client = Client(reactor)
    d = client.run(concurrency, duration)
    return d


if __name__ == '__main__':
    import sys
    driver(main, sys.argv)
