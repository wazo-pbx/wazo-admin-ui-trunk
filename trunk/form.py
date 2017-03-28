# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_wtf import FlaskForm

from wtforms.fields import SubmitField
from wtforms.fields import StringField

from wtforms.validators import InputRequired


class TrunkForm(FlaskForm):
    name = StringField('Name', [InputRequired()])
    submit = SubmitField('Submit')
