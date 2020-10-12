

class BadArgumentError(Exception):
    pass


class RequestError(Exception):
    pass


class FailedPOSTRequest(RequestError):
    pass
