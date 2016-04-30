import logging

from django.contrib import messages
from django.shortcuts import redirect

from apps import BaseView
from apps.home.forms import ContactForm

logger = logging.getLogger(__name__)


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


class TermsView(BaseView):
    template_name = 'home/terms.html'

    def get(self, request, *args, **kwargs):
        return self._render(
            title='Terms & Conditions',
            request=request,
        )


class ContactView(BaseView):
    form_class = ContactForm
    template_name = 'home/contact.html'

    def get(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(initial=self.initial)

        return self._render(
            request=request,
            form=form,
        )

    def post(self, request, *args, **kwargs):
        # Init the form
        form = self.form_class(request.POST)

        # Validate POST data
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
            )

        # Push success message and redirect back
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('home:contact')

    def _render(self, request, form):
        return super(ContactView, self)._render(
            request=request,
            form=form,
            title='Contact',
        )
