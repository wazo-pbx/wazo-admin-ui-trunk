# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from flask_menu.classy import classy_menu_item
from marshmallow import fields

from wazo_admin_ui.helpers.classful import BaseView
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
