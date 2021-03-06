"""
    Forms
    ~~~~~
"""

from flask_wtf import Form
from wtforms import BooleanField, SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.profilemanager import User
from wiki.web.profilemanager import db


class URLForm(FlaskForm):
    url = StringField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(FlaskForm):
    term = StringField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(FlaskForm):
    title = StringField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = StringField('')



# class LoginForm(Form):
#     name = TextField('', [InputRequired()])
#     password = PasswordField('', [InputRequired()])
#
#     def validate_name(form, field):
#         user = current_users.get_user(field.data)
#         if not user:
#             raise ValidationError('This username does not exist.')
#
#     def validate_password(form, field):
#         user = current_users.get_user(form.name.data)
#         if not user:
#             return
#         if not user.check_password(field.data):
#             raise ValidationError('Username and password do not match.')


class CreateProfileForm(Form):
    name = StringField(u'Full Name', [InputRequired()])
    username = StringField(u'Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    email = EmailField(u'Email', [InputRequired()])
    phone = StringField(u'Phone Number', [InputRequired()])
    address = StringField(u'Address', [InputRequired])
    submit = SubmitField("Submit Profile")


class SignInForm(Form):
    name = StringField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

