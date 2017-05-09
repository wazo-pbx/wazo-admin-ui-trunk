# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask import jsonify, request
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.classful import LoginRequiredView
from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response

from .form import TrunkForm


class TrunkView(BaseView):

    form = TrunkForm
    resource = 'trunk'

    @classy_menu_item('.trunks', 'Trunks', order=4, icon="server")
    def index(self):
        return super(TrunkView, self).index()

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('trunk', {}))
        return form


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
