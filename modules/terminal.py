import termios, sys, os
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
from time import sleep


def coroutine(f):
    def wrap(*args,**kwargs):
        gen = f(*args,**kwargs)
        gen.send(None)
        return gen
    return wrap


def getch(n=1):
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl(fd, F_GETFL)
    fcntl(fd, F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while n > 0:
            sleep(0.01)
            try:
                c = sys.stdin.read(1)
                n -= 1
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl(fd, F_SETFL, oldflags)


def myreadstr(fd):
    flags = fcntl(fd, F_GETFL)
    fcntl(fd, F_SETFL, flags | O_NONBLOCK)
    retval = 0
    string = str()
    try:
        string = fd.readline()
    except (OSError, IOError):
        retval = 1
        pass

    return retval, string


@coroutine
def read_file(fd, func):
    while True:
        line = fd.readline()
        if not line:
            break
        func(line)
    yield 0
