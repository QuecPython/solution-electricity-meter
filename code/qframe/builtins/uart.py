from .. import AppExtensionABC
from ..threading import Thread
from ..serial import Serial as _Serial
from ..logging import getLogger

logger = getLogger(__name__)


class Uart(AppExtensionABC):

    def __init__(self, name, app=None):
        self.serial = None
        self.write = None
        self.read = None
        self.listen_thread = None
        super().__init__(name, app=app)

    def init_app(self, app):
        self.serial = _Serial(**app.config['UART'])
        self.write = self.serial.write
        self.read = self.serial.read
        self.listen_thread = Thread(target=self.listen_thread_worker)
        app.append_extension(self)

    def load(self):
        self.serial.open()
        self.listen_thread.start()

    def listen_thread_worker(self):
        while True:
            try:
                data = self.read(1024)
            except Exception as e:
                logger.error('serial read error: {}'.format(e))
            else:
                try:
                    self.recv_callback(data)
                except Exception as e:
                    logger.error('recv_callback error: {}'.format(e))

    def recv_callback(self, data):
        raise NotImplementedError('you must implement this method to handle data received from device.')
