from __future__ import absolute_import

from apps import BaseView


class AlarmView(BaseView):

    def _set_form_choices(self, form, regions):
        form.fields['region'].choices = (
            (str(r['id']), r['name'])
            for r in regions['_embedded']['regions'])