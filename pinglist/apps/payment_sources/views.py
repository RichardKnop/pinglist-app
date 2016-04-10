import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.utils.dateparse import parse_datetime

from lib.auth import logged_in
from apps import BaseView
from apps.payment_sources.forms import (
    AddCardForm,
    DeleteCardForm
)


logger = logging.getLogger(__name__)


class IndexView(BaseView):
    template_name = 'payment_sources/index.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        # Fetch the cards
        cards = self.api.list_cards(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )
        # Parse datetime strings
        for card in cards['_embedded']['cards']:
            card['created_at'] = parse_datetime(card['created_at'])
            card['updated_at'] = parse_datetime(card['updated_at'])

        return self._render(
            request=request,
            title='Payment Sources',
            active_link='payment_sources',
            cards=cards,
        )


class AddView(BaseView):
    form_class = AddCardForm
    template_name = 'payment_sources/add.html'

    @logged_in
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

        return self._render_add_payment_source(request=request, form=form)

    @logged_in
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        # Add the card
        try:
            self.api.add_card(
                access_token=request.session['access_token']['access_token'],
                token=form.cleaned_data['stripe_token'],
            )

            messages.success(request, 'Card added successfully')
            return redirect('payment_sources:index')

        # Adding card failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(request=request, form=form)

    def _render(self, request, form):
        return super(AddView, self)._render(
            request=request,
            form=form,
            title='Add Payment Source',
            active_link='payment_sources',
            stripe_publishable_key=settings.STRIPE_PUBLISHABLE_KEY,
        )


class DeleteView(BaseView):
    form_class = DeleteCardForm
    template_name = 'payment_sources/delete.html'

    @logged_in
    def get(self, request, card_id, *args, **kwargs):
        # Get the card
        try:
            self.api.get_card(
                access_token=request.session['access_token']['access_token'],
                card_id=card_id,
            )

        # Card not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        form = self.form_class(initial={'card_id': card_id})

        return self._render_delete_payment_source(
            request=request, form=form, card_id=card_id)

    @logged_in
    def post(self, request, card_id, *args, **kwargs):
        # Get the card
        try:
            self.api.get_card(
                access_token=request.session['access_token']['access_token'],
                card_id=card_id,
            )

        # Card not found
        except self.api.APIError as e:
            logger.debug(str(e))
            return HttpResponseNotFound()

        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(
                request=request,
                form=form,
                card_id=card_id,
            )

        # Delete the card
        try:
            self.api.delete_card(
                access_token=request.session['access_token']['access_token'],
                card_id=card_id,
            )

            messages.success(request, 'Card deleted successfully')
            return redirect('payment_sources:index')

        # Deleting card failed
        except self.api.APIError as e:
            logger.debug(str(e))
            form.add_error(None, str(e))
            return self._render(
                request=request,
                form=form,
                card_id=card_id,
            )

    def _render(self, request, form, card_id):
        return super(AddView, self)._render(
            request=request,
            form=form,
            card_id=card_id,
            title='Delete Payment Source',
            active_link='payment_sources',
        )