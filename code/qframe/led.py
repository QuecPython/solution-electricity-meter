import utime
from machine import Pin
from .threading import Thread, Semaphore, Lock


class Led(object):

    def __init__(self, GPIOn):
        self.__led = Pin(
            getattr(Pin, 'GPIO{}'.format(GPIOn)),
            Pin.OUT,
            Pin.PULL_PD,
            0
        )
        self.__off_remaining = 1000
        self.__on_remaining = 1000
        self.__running_sem = Semaphore(value=0)
        self.__blink_lock = Lock()
        self.__blink_thread = Thread(target=self.__blink_thread_worker)

    def on(self):
        self.__led.write(1)

    def off(self):
        self.__led.write(0)

    def blink(self, on_remaining, off_remaining, count):
        """start LED blink"""
        with self.__blink_lock:
            self.__on_remaining = on_remaining
            self.__off_remaining = off_remaining
            self.__blink_thread.start()
        self.__running_sem.clear()
        self.__running_sem.release(count)

    def __blink_thread_worker(self):
        while True:
            self.__running_sem.acquire()
            with self.__blink_lock:
                on_remaining = self.__on_remaining
                off_remaining = self.__off_remaining
            self.on()
            utime.sleep_ms(on_remaining)
            self.off()
            utime.sleep_ms(off_remaining)
