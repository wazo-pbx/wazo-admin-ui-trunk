# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wtforms.fields import SubmitField
from wtforms.fields import StringField
from wtforms.validators import InputRequired

from wazo_admin_ui.helpers.form import BaseForm


class TrunkForm(BaseForm):
    name = StringField('Name', [InputRequired()])
    submit = SubmitField('Submit')
