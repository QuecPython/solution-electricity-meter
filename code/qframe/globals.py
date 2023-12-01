from .threading import Lock


class ContextVar(object):
    """Context Variable"""
    __storage__ = {}
    __lock__ = Lock()

    def __init__(self, ident, error_msg=None):
        self.__ident = ident
        self.__error_msg = error_msg or '\"{}\" cannot be found in the current context'.format(self.ident)

    @property
    def ident(self):
        if callable(self.__ident):
            return self.__ident()
        return self.__ident

    def set(self, value):
        with self.__lock__:
            self.__storage__[self.ident] = value

    def get(self):
        with self.__lock__:
            if self.ident not in self.__storage__:
                raise RuntimeError(self.__error_msg)
            return self.__storage__[self.ident]

    def __call__(self, *args, **kwargs):
        return self.get()


class _AppCtxGlobals(object):

    def setdefault(self, name, value):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            setattr(self, name, value)
            return value

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return default

    def set(self, name, value):
        setattr(self, name, value)


_no_app_msg = 'Working outside of application context.'
CurrentApp = ContextVar('Application', error_msg=_no_app_msg)
G = ContextVar('_AppCtxGlobals', error_msg=_no_app_msg)
