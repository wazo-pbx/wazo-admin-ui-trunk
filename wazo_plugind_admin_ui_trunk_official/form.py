# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    SubmitField,
    StringField,
    BooleanField,
    SelectField,
    HiddenField,
    FieldList,
    FormField
)
from wtforms.validators import InputRequired, Length

from wazo_admin_ui.helpers.form import BaseForm


class EnpointCustomForm(BaseForm):
    id = HiddenField()
    interface = StringField(l_('Interface'), validators=[InputRequired()])


class OptionsForm(BaseForm):
    option_key = StringField(validators=[InputRequired()])
    option_value = StringField(validators=[InputRequired()])


class EnpointSipForm(BaseForm):
    id = HiddenField()
    username = StringField(l_('Username'), validators=[InputRequired(), Length(max=40)])
    secret = StringField(l_('Secret'), validators=[InputRequired(), Length(max=80)])
    type = SelectField(l_('Type'), choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))])
    host = SelectField(l_('Host'), validators=[InputRequired(), Length(max=255)],
                       choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))])
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class EnpointIaxForm(BaseForm):
    id = HiddenField()
    name = StringField(l_('Name'), validators=[InputRequired(), Length(max=40)])
    type = SelectField(l_('Type'), choices=[('user', l_('User')), ('peer', l_('Peer')), ('friend', l_('Friend'))])
    host = SelectField(l_('Host'), validators=[InputRequired(), Length(max=255)],
                       choices=[('dynamic', l_('Dynamic')), ('static', l_('Static'))])
    host_value = StringField('', validators=[Length(max=255)])
    options = FieldList(FormField(OptionsForm))


class TrunkForm(BaseForm):
    context = SelectField(l_('Context'), choices=[])
    protocol = SelectField(choices=[('sip', l_('SIP')),('iax', l_('IAX')), ('custom', l_('CUSTOM'))])
    twilio_incoming = BooleanField(l_('Twilio Incoming'), default=False)
    endpoint_sip = FormField(EnpointSipForm)
    endpoint_iax = FormField(EnpointIaxForm)
    endpoint_custom = FormField(EnpointCustomForm)
    submit = SubmitField(l_('Submit'))
