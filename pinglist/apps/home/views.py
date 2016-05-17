import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseServerError

from apps import BaseView
from apps.home.models import FAQ
from apps.home.forms import ContactForm

logger = logging.getLogger('django')


class IndexView(BaseView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        # Fetch subscription plans
        try:
            plans = self.api.list_plans()

        # Fetching subscription plans failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # We only want to display maximum of 4 plans on the homepage
        plans["_embedded"]["plans"] = plans["_embedded"]["plans"][:4]

        return self._render(
            title='Pinglist - Uptime And Performance Monitoring Done Right',
            request=request,
            plans=plans,
        )


class FAQView(BaseView):
    template_name = 'home/faq.html'

    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.all()
        return self._render(
            title='Frequently Asked Questions - Pinglist',
            request=request,
            faqs=faqs,
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

            # Fire off the contact email
        try:
            self.api.contact(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )

        # Sending contact email failed
        except self.api.APIError as e:
            logger.error(str(e))
            return HttpResponseServerError()

        # Push success message and redirect back
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('home:contact')

    def _render(self, request, form):
        return super(ContactView, self)._render(
            request=request,
            form=form,
            title='Contact - Pinglist',
        )
