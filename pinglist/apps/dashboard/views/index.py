from . import BaseView


class IndexView(BaseView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        return self._render(request=request)