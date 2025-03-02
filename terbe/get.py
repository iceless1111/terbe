import socket, struct, sys, getpass, platform
from argparse import Namespace
getUsername = getpass.getuser
getHostname = platform.node

def NetInfo():
    namespace = Namespace()
    namespace.hostname = socket.gethostname()
    namespace.ip = socket.gethostbyname(namespace.hostname)
    namespace.mask = socket.inet_ntoa(struct.pack(">L", (1<<32) - (1<<32>>24))) 
    return namespace

def Char():
    try:
        from msvcrt import getch
        return getch()
    except ImportError:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)