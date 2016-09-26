from nose.tools import assert_raises

from eventlet import sleep, spawn
from eventlet.hubs import get_hub, IOClosed
from eventlet.green.select import select
from eventlet.green.socket import socket


def test_mark_file_as_reopened():
    # Fix API inconsistency in select and Hub.
    # mark_as_closed takes one argument, but called without arguments.
    # on_error takes file descriptor, but called with an exception object.
    s = socket()
    try:
        s.setblocking(0)
        s.bind(('127.0.0.1', 0))
        s.listen(5)

        gt = spawn(select, [s], [s], [s])
        sleep(0)
        hub = get_hub()

        hub.mark_as_reopened(s.fileno())
        with assert_raises(IOClosed):
            sleep(0)
    finally:
        s.close()
