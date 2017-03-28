# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint

from .service import TrunkService
from .view import TrunkView

trunk = create_blueprint('trunk', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        config = dependencies['config']

        TrunkView.service = TrunkService(config['confd'])
        TrunkView.register(trunk, route_base='/trunks')
        register_flaskview(trunk, TrunkView)

        core.register_blueprint(trunk)
