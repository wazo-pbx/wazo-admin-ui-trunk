# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView, BaseDestinationView
from wazo_admin_ui.helpers.mallow import BaseSchema, BaseAggregatorSchema, extract_form_fields

from .form import TrunkForm


class TrunkSchema(BaseSchema):

    class Meta:
        fields = extract_form_fields(TrunkForm)


class AggregatorSchema(BaseAggregatorSchema):
    _main_resource = 'trunk'

    trunk = fields.Nested(TrunkSchema)


class TrunkView(BaseView):

    form = TrunkForm
    resource = 'trunk'
    schema = AggregatorSchema

    @classy_menu_item('.trunks', 'Trunks', order=4, icon="server")
    def index(self):
        return super(TrunkView, self).index()


class TrunkDestinationView(BaseDestinationView):

    def list_json(self):
        params = self._extract_params()
        trunks = self.service.list(**params)
        results = self._populate_list(trunks['items'])
        return self._select2_response(results, trunks['total'], params)

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
