from __future__ import division, print_function

import perf

from performance.benchmarks.bench_twisted.benchlib import multidriver
from performance.benchmarks.bench_twisted import accepts, iteration, names, pb, tcp, threads, web


BENCHMARKS = {
    'accepts': accepts.main,
    'iteration': iteration.main,
    'names': names.main,
    'pb': pb.main,
    'tcp': tcp.main,
    'threads': threads.main,
    'web': web.main,
}

# Skipped: 'accepts', 'threads', 'web'
DEFAULT_BENCHMARKS = ['iteration', 'names', 'pb', 'tcp']


def bench_twisted(benchmarks):
    multidriver(*benchmarks)


def add_cmdline_args(cmd, args):
    cmd.append(args.benchmarks)


if __name__ == "__main__":
    runner = perf.Runner(add_cmdline_args=add_cmdline_args)
    runner.metadata['description'] = "Create chaosgame-like fractals"
    cmd = runner.argparser
    choices = list(BENCHMARKS) + ["all"]
    cmd.add_argument("benchmark", nargs='?', choices=sorted(choices),
                     help="Benchmark name, default: %s"
                          % ', '.join(DEFAULT_BENCHMARKS))

    args = runner.parse_args()

    if not args.benchmark:
        benchmarks = DEFAULT_BENCHMARKS
    if args.benchmark == "all":
        benchmarks = sorted(BENCHMARKS)
    else:
        benchmarks = [args.benchmark]

    bench_twisted(benchmarks)
