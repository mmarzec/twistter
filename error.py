class ApiError(Exception):
    STATUS_CODE = 500

    def __init__(self, message, **kwargs):
        Exception.__init__(self, message)
        self.extra_fields = kwargs

    @property
    def json(self):
        ret = {
            'status': 'error',
            'message': self.message
        }
        ret.update(self.extra_fields)
        return ret


class BadRequest(ApiError):
    STATUS_CODE = 400


class NotFound(ApiError):
    STATUS_CODE = 404


class Gone(ApiError):
    STATUS_CODE = 410


class BadGateway(ApiError):
    STATUS_CODE = 502


class ServiceNotAvailable(ApiError):
    STATUS_CODE = 503


class Unauthorized(ApiError):
    STATUS_CODE = 401


class MethodNotAllowed(ApiError):
    STATUS_CODE = 405

