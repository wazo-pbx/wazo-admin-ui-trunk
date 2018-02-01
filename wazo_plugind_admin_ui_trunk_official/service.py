# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class TrunkService(BaseConfdService):
    resource_confd = 'trunks'

    def get_context(self, context):
        result = confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_endpoint_sip(self, endpoint_id):
        return confd.endpoints_sip.get(endpoint_id)

    def get_endpoint_iax(self, endpoint_id):
        return confd.endpoints_iax.get(endpoint_id)

    def get_endpoint_custom(self, endpoint_id):
        return confd.endpoints_custom.get(endpoint_id)

    def create(self, resource):
        resource_created = super(TrunkService, self).create(resource)
        resource['id'] = resource_created['id']
        if resource.get('endpoint_sip'):
            endpoint_sip = confd.endpoints_sip.create(resource['endpoint_sip'])
            confd.trunks(resource['id']).add_endpoint_sip(endpoint_sip['id'])
        if resource.get('endpoint_iax'):
            endpoint_iax = confd.endpoints_iax.create(resource['endpoint_iax'])
            confd.trunks(resource['id']).add_endpoint_iax(endpoint_iax['id'])
        if resource.get('endpoint_custom'):
            endpoint_custom = confd.endpoints_custom.create(resource['endpoint_custom'])
            confd.trunks(resource['id']).add_endpoint_custom(endpoint_custom['id'])

    def update(self, resource):
        super(TrunkService, self).update(resource)
        if resource.get('endpoint_sip'):
            confd.endpoints_sip.update(resource['endpoint_sip'])
        if resource.get('endpoint_iax'):
            confd.endpoints_iax.update(resource['endpoint_iax'])
        if resource.get('endpoint_custom'):
            confd.endpoints_custom.update(resource['endpoint_custom'])
