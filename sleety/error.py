class SleetyError(Exception):
    pass


class SleetyAuthError(SleetyError):
    pass


class SleetyUnsupportedError(SleetyError):
    pass


class SleetySchemaError(SleetyError):
    pass
