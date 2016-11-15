from __future__ import division, with_statement, print_function, absolute_import

from performance.benchmarks.bench_twisted.benchlib import Client, driver


class Client(Client):

    def _request(self):
        self._reactor.callLater(0.0, self._continue, None)


def main(reactor, duration):
    concurrency = 10

    client = Client(reactor)
    d = client.run(concurrency, duration)
    return d


if __name__ == '__main__':
    import sys
    driver(main, sys.argv)
