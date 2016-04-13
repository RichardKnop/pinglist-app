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

    def _set_form_choices(self, form, plans):
        form.fields['plan'].choices = (
            (str(p['id']), self._short_plan_desc(p))
            for p in plans['_embedded']['plans'])