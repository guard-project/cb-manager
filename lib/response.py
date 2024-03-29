from lib.http import HTTP_Status
from utils.exception import extract_info
from utils.log import Log
from utils.sequence import expand, is_list
from utils.stack import info


class BaseResponse(object):
    error = False
    log_level = "info"
    code = None

    def __init__(self, message, error=False, exception=None, **kwargs):
        self.log = Log.get(self.__class__.__name__)
        self.data = {"message": message}
        if exception is not None:
            self.data.update(exception=extract_info(exception))
        self.data.update(kwargs)

    def __data(self):
        return expand(
            self.data, status=self.status(), code=self.code, error=self.error
        )

    def __str__(self):
        return self.status()

    def __int__(self):
        return self.code

    def __dict__(self):
        return self.__data()

    def __log(self):
        if self.log_level is not None:
            _exception = self.data.get("exception", None)
            _info = info(level=3)
            self.log.notice(f"@{_info.filename}:{_info.lineno}")
            _msg = self.data.get("message", "No message")
            if _exception is not None:
                self.log.exception(_msg, _exception)
            else:
                getattr(self.log, self.log_level)(_msg)

    @classmethod
    def status(cls):
        return cls.code.phrase

    def apply(self, resp):
        self.__log()
        resp.media = self.__data()
        resp.status = f"{self.code} {self}"

    def add(self, resp):
        self.__log()
        if is_list(resp):
            resp.append(self.__data())
        else:
            if not is_list(resp.media):
                resp.media = []
            resp.media.append(self.__data())
            resp_code = int(resp.status.split()[0])
            if self.code is not None and HTTP_Status.gt(resp_code, self.code):
                resp.status = f"{self.code} {self.status()}"

    def update(self, **kwargs):
        self.data.update(kwargs)


class BadRequestResponse(BaseResponse):
    code = HTTP_Status.BAD_REQUEST
    error = True
    log_level = "error"

    def __init__(self, exception=None, **kwargs):
        title = (
            exception.title if exception is not None else "Request not valid"
        )  # noqa: E501
        super().__init__(title, exception, **kwargs)


class ConflictResponse(BaseResponse):
    code = HTTP_Status.CONFLICT
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class CreatedResponse(BaseResponse):
    code = HTTP_Status.CREATED
    log_level = "success"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class InternalServerErrorResponse(BaseResponse):
    code = HTTP_Status.INTERNAL_SERVER_ERROR
    error = True
    log_level = "error"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class NotAcceptableResponse(BaseResponse):
    code = HTTP_Status.NOT_ACCEPTABLE
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NoContentResponse(BaseResponse):
    code = HTTP_Status.NO_CONTENT
    log_level = "warning"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NotFoundResponse(BaseResponse):
    code = HTTP_Status.NOT_FOUND
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class NotModifiedResponse(BaseResponse):
    code = HTTP_Status.NOT_MODIFIED
    log_level = "warning"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class OkResponse(BaseResponse):
    code = HTTP_Status.OK
    log_level = "success"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class ContentResponse(OkResponse):
    log_level = None

    def __init__(self, content):
        self.data = content

    def apply(self, resp):
        resp.media = self.data
        resp.status = f"{self.code} {self}"


class ResetContentResponse(BaseResponse):
    code = HTTP_Status.RESET_CONTENT
    log_level = "warn"

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)


class UnauthorizedResponse(BaseResponse):
    code = HTTP_Status.UNAUTHORIZED
    error = True
    log_level = "error"

    def __init__(self):
        super().__init__(message="Authentication failed")

    def apply(self, resp):
        super().apply(resp)
        resp.complete = True


class UnprocEntityResponse(BaseResponse):
    code = HTTP_Status.UNPROCESSABLE_ENTITY
    error = True
    log_level = "error"

    def __init__(self, message, exception=None, **kwargs):
        super().__init__(message, exception=exception, **kwargs)


class UnsuppMediaTypeResponse(BaseResponse):
    code = HTTP_Status.UNSUPPORTED_MEDIA_TYPE
    error = True
    log_level = "error"

    def __init__(self, exception=None, **kwargs):
        title = (
            exception.title
            if exception is not None
            else "Unsupported media type"
        )  # noqa: E501
        super().__init__(title, exception=exception, **kwargs)
