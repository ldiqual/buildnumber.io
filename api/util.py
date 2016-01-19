import sys

from django.template.loader import render_to_string
from rest_framework import exceptions
from buildnumber import settings
from camel_snake_kebab import camelCase
import requests

from models import Build

def assert_valid_extra(extra, rawExtra):

    if len(rawExtra) > 1024:
        raise exceptions.ValidationError("Payload must not exceed 1024 bytes")

    # Make sure no reserved field name is in there
    reserved_field_names = set([field.name for field in Build._meta.get_fields()])
    reserved_field_names.update([camelCase(field.name) for field in Build._meta.get_fields()])
    reserved_field_names.update(set(['pk']))

    if len(set(reserved_field_names).intersection(extra.keys())) != 0:
        error = "Additional data must not contained any of the following reserved keys: %s" % (", ".join(reserved_field_names),)
        raise exceptions.ValidationError(error)

def send_welcome_email(account, account_email, api_key):

    template_context = {
        'title': "Welcome to buildnumber.io!",
        'api_key': api_key.key
    }
    text_content = render_to_string('welcome-email.txt', template_context)
    html_content = render_to_string('welcome-email-inlined.html', template_context)

    key = settings.MAILGUN_SECRET_API_KEY
    domain = settings.MAILGUN_DOMAIN
    data = {
        'from': 'Buildnumber.io <welcome@buildnumber.io>',
        'to': account_email.email,
        'subject': 'Your buildnumber.io API token',
        'text': text_content,
        'html': html_content
    }
    request = requests.post('https://api.mailgun.net/v3/%s/messages' % (domain,), data=data, auth=('api', key))

    return request.status_code == requests.codes.ok
