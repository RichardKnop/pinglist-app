from __future__ import absolute_import

from apps import BaseView


class SubscriptionView(BaseView):

    def _short_plan_desc(self, plan):
        return '{} - ${}'.format(
            plan['name'],
            format(float(plan['amount']) / float(100), '.2f'),
        )

    def _short_card_desc(self, card):
        return '{} ending with {}'.format(
            card['brand'].upper(),
            card['last_four'],
        )

    def _set_form_choices(self, request, form):
        # Fetch the plans
        plans = self.api.list_plans()

        # Fetch the cards
        cards = self.api.list_cards(
            access_token=request.session['access_token']['access_token'],
            user_id=request.session['access_token']['user_id'],
        )

        # Load form select options
        form.fields['plan'].choices = (
            (str(p['id']), self._short_plan_desc(p))
            for p in plans['_embedded']['plans'])
        form.fields['payment_source'].choices = (
            (str(c['id']), self._short_card_desc(c))
            for c in cards['_embedded']['cards'])