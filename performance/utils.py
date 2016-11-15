import contextlib
import errno
import os
import tempfile


@contextlib.contextmanager
def temporary_file():
    tmp_filename = tempfile.mktemp()
    try:
        yield tmp_filename
    finally:
        try:
            os.unlink(tmp_filename)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise


def create_environ():
    env = {}
    for name in ("PATH", "HOME", "TEMP", "COMSPEC", "SystemRoot"):
        if name in os.environ:
            env[name] = os.environ[name]
    return env
