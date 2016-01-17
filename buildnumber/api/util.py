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

    key = settings.MAILGUN_SECRET_API_KEY
    domain = settings.MAILGUN_DOMAIN
    data = {
        'from': 'Buildnumber.io <welcome@buildnumber.io>',
        'to': account_email.email,
        'subject': 'Create a new build on Buildnumber.io',
        'text': 'Your api token: %s' % (api_key.key,)
    }
    request = requests.post('https://api.mailgun.net/v3/%s/messages' % (domain,), data=data, auth=('api', key))

    return request.status_code == requests.codes.ok
