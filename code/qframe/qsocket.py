import usocket
from .logging import getLogger
from .threading import Lock

logger = getLogger(__name__)


class TcpSocket(object):
    socket_type = usocket.SOCK_STREAM

    class TimeoutError(Exception):
        pass

    def __init__(self, host, port, timeout=None, keep_alive=None):
        self.__host = host
        self.__port = port
        self.__ip = None
        self.__family = None
        self.__domain = None
        self.__timeout = timeout
        self.__keep_alive = keep_alive
        self.__sock = None

    def __str__(self):
        return '{}(host=\"{}\",port={})'.format(type(self).__name__, self.__host, self.__port)

    @property
    def sock(self):
        if self.__sock is None:
            raise ValueError('Socket Unbound Error')
        return self.__sock

    def __init_args(self):
        rv = usocket.getaddrinfo(self.__host, self.__port)
        if not rv:
            raise ValueError('DNS detect error')
        self.__family = rv[0][0]
        self.__domain = rv[0][3]
        self.__ip, self.__port = rv[0][4]

    def connect(self):
        self.__init_args()
        self.__sock = usocket.socket(self.__family, self.socket_type)
        self.__sock.connect((self.__ip, self.__port))
        if self.__timeout and self.__timeout > 0:
            self.__sock.settimeout(self.__timeout)
        if self.__keep_alive and self.__keep_alive > 0:
            self.__sock.setsockopt(usocket.SOL_SOCKET, usocket.TCP_KEEPALIVE, self.__keep_alive)

    def disconnect(self):
        if self.__sock:
            self.__sock.close()
            self.__sock = None

    def write(self, data):
        return self.sock.send(data) == len(data)

    def read(self, size=1024):
        try:
            return self.sock.recv(size)
        except Exception as e:
            if isinstance(e, OSError) and e.args[0] == 110:
                # read timeout.
                raise self.TimeoutError(str(self))
            else:
                raise e

    @property
    def status_code(self):
        if self.__sock is None:
            return 99
        return self.__sock.getsocketsta()


class UdpSocket(TcpSocket):
    socket_type = usocket.SOCK_DGRAM

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__status_code = 0
        self.__lock = Lock()

    @property
    def status_code(self):
        with self.__lock:
            return self.__status_code

    @status_code.setter
    def status_code(self, code):
        with self.__lock:
            self.__status_code = code

    def write(self, data):
        try:
            return super().write(data)
        except Exception as e:
            self.status_code = 99
            raise e

    def read(self, size=1024):
        try:
            return super().read(size=size)
        except Exception as e:
            if not isinstance(e, self.TimeoutError):
                self.status_code = 98
            raise e
