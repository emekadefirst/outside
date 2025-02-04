from starlette.middleware import Middleware


class LogMiddleware(Middleware):
    def __init__(self, request):
        pass