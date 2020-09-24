class const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


class env:
    pass


const.UVICORN_PRO_PORT = 80
const.UVICORN_PRO_RELOAD = True
const.UVICORN_DEV_PORT = 8000
const.UVICORN_DEV_RELOAD = False
###aaaasdjbjbjygfjohihihhasdfaaaadsfaaass
