from lib.auth import is_logged_in


class AccessTokenMiddleware(object):

    def process_request(self, request):
        request.logged_in = is_logged_in(request)
