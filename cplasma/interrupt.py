import signal

class BlockSigint(object):
    def __init__(self):
        self.__handler = signal.signal(signal.SIGINT, signal.SIG_DFL)

    def __del__(self):
        signal.signal(signal.SIGINT, self.__handler)

