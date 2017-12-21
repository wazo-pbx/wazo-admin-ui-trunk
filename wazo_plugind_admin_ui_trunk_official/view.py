# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from flask import jsonify, request, render_template
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import (LoginRequiredView,
                                            BaseView,
                                            NewViewMixin,
                                            extract_select2_params,
                                            build_select2_response)
from wazo_admin_ui.helpers.destination import listing_urls

from .form import TrunkForm


class TrunkView(BaseView):
    form = TrunkForm
    resource = 'trunk'

    @classy_menu_item('.trunks', l_('Trunks'), order=4, icon="server")
    def index(self):
        return super(TrunkView, self).index()

    def new(self, protocol, form=None):
        if protocol not in ['sip', 'custom']:
            return self._index(form)

        form = form or self.form()
        return render_template(self._get_template('protocol_{}'.format(protocol)),
                               form=form,
                               listing_urls=listing_urls)

    def _map_resources_to_form(self, resource):
        endpoint_sip = endpoint_custom = protocol = None
        if resource['endpoint_sip']:
            protocol = 'sip'
            endpoint_sip = self.service.get_endpoint_sip(resource['endpoint_sip']['id'])
            if endpoint_sip['host'] != 'dynamic':
                endpoint_sip['host_value'] = endpoint_sip['host']
                endpoint_sip['host'] = 'static'
            endpoint_sip['options'] = self._build_sip_options(endpoint_sip['options'])
        elif resource['endpoint_custom']:
            protocol = 'custom'
            endpoint_custom = self.service.get_endpoint_custom(resource['endpoint_custom']['id'])
        form = self.form(data=resource,
                         protocol=protocol,
                         endpoint_sip=endpoint_sip,
                         endpoint_custom=endpoint_custom)
        return form

    def _build_sip_options(self, options):
        result = []
        for option in options:
            result.append({'option_key': option[0],
                           'option_value': option[1]})

        return result

    def _populate_form(self, form):
        form.context.choices = self._build_set_choices_context(form.context)
        return form

    def _build_set_choices_context(self, context_form):
        if not context_form.data or context_form.data == 'None':
            return []
        else:
            context = self.service.get_context(context_form.data)
            if context:
                return [(context['name'], context['label'])]

        return [(context_form.data, context_form.data)]

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('trunk', {}))
        return form

    def _map_form_to_resources(self, form, form_id=None):
        resource = super(TrunkView, self)._map_form_to_resources(form, form_id)
        if 'username' in resource['endpoint_sip']:
            resource = self._map_form_to_resource_sip_options(form, resource)
            if resource['endpoint_sip']['host'] == 'static':
                resource['endpoint_sip']['host'] = form.endpoint_sip.host_value.data
            del resource['endpoint_custom']
        elif 'interface' in resource['endpoint_custom']:
            del resource['endpoint_sip']

        return resource

    def _map_form_to_resource_sip_options(self, form, resource):
        options = []
        for option in resource['endpoint_sip']['options']:
            options.append([option['option_key'], option['option_value']])

        resource['endpoint_sip']['options'] = options
        return resource


class TrunkListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        trunks = self.service.list(**params)
        results = self._populate_list(trunks['items'])
        return jsonify(build_select2_response(results, trunks['total'], params))

    def _populate_list(self, trunks):
        results = []
        for trunk in trunks:
            if trunk.get('endpoint_custom'):
                text = '{} ({})'.format(trunk['endpoint_custom']['interface'], 'custom')
            if trunk.get('endpoint_sip'):
                text = '{} ({})'.format(trunk['endpoint_sip']['username'], 'sip')
            if trunk.get('endpoint_iax'):
                text = '{} ({})'.format(trunk['endpoint_iax']['username'], 'iax')
            results.append({'id': trunk['id'], 'text': text})
        return results
