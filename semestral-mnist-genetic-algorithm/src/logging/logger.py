class Logger:
    instance = None

    class __Logger:
        def __init__(self, path: str, mode: str):
            self.path = '../output/log/' + path
            self.mode = mode
            self.do = True

    def __init__(self, path: str = '', mode: str = ''):
        if Logger.instance is None:
            Logger.instance = Logger.__Logger(path, mode)
        else:
            Logger.instance.mode = mode

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def log(self, information: str):
        if not self.do:
            return
        with open(self.path, 'a+') as logger:
            line = '[' + self.mode + '] ' + information + '\n'
            logger.write(line)
            # print(line)
