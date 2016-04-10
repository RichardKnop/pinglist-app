from apps import BaseView


class IndexView(BaseView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        # Fetch the plans
        plans = self.api.list_plans()

        # We only want to display maximum of 4 plans on the homepage
        plans["_embedded"]["plans"] = plans["_embedded"]["plans"][:4]

        return self._render(
            request=request,
            plans=plans,
        )