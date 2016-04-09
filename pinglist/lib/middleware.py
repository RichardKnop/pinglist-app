class LoggedInFlagMiddleware(object):

    def process_request(self, request):
        try:
            request.session['access_token']
            request.session['access_token_granted_at']
            request.logged_in = True
        except KeyError:
            request.logged_in = False