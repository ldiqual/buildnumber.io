from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.decorators import api_view

from serializers import *
from models import *
from util import assert_valid_extra, send_welcome_email

@api_view(http_method_names=['GET'])
def get_last_build(request, package_name):

    key = request.GET.get('token', None)

    # Make sure an API key is provided
    if not key:
        raise exceptions.NotAuthenticated("You must provide `?token=API_TOKEN` to use this service. Please check your emails to get this token.")

    # Grab the API key model, make sure it exists
    try:
        api_key = ApiKey.objects.get(key=key)
    except ApiKey.DoesNotExist:
        raise exceptions.AuthenticationFailed("This API token doesn't exist")

    package = get_object_or_404(Package, name=package_name)
    last_build = package.builds.order_by('-build_number').first()

    if not last_build:
        raise exceptions.NotFound("Couldn't find a build for this package name")

    # Serialize the new build
    serializer = BuildSerializer(last_build)
    response_data = serializer.data.copy()
    response_data.update(last_build.extra)

    return Response(response_data)

@api_view(http_method_names=['POST'])
def create_build(request, package_name, format=None):

    body = request.body
    key = request.GET.get('token', None)
    output = request.GET.get('output', 'json')
    extra = request.data if request.data else {}

    # Make sure we have a valid output format
    if not output in ['json', 'buildNumber']:
        return HttpResponseBadRequest("`output` must be 'json' or 'buildNumber' (default is 'json')")

    assert_valid_extra(extra, body)

    # Make sure an API key is provided
    if not key:
        raise exceptions.NotAuthenticated("You must provide `?token=API_TOKEN` to use this service. Please check your emails to get this token.")

    # Grab the API key model, make sure it exists
    try:
        api_key = ApiKey.objects.get(key=key)
    except ApiKey.DoesNotExist:
        raise exceptions.AuthenticationFailed("This API token doesn't exist")

    # Grab the corresponding package, create it if it doesn't exist
    try:
        package = Package.objects.get(name=package_name, account=api_key.account)
    except Package.DoesNotExist:
        package = Package(name=package_name, account=api_key.account)
        package.save()

    # Get the last build to infer the new build number from
    last_build = package.builds.order_by('-build_number').first()

    # Create a new build
    new_build_number = last_build.build_number + 1 if last_build else 1
    new_build = Build(package = package, build_number=new_build_number)
    new_build.extra = extra
    new_build.save()

    if output == 'buildNumber':
        response = Response(new_build.build_number, content_type='plain/text')
        #response['Content-Type'] = 'plain/text'
        return response

    # Serialize the new build
    serializer = BuildSerializer(new_build)
    response_data = serializer.data.copy()
    response_data.update(new_build.extra)

    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET'])
def get_build(request, package_name, build_number, format=None):

    key = request.GET.get('token', None)

    # Make sure an API key is provided
    if not key:
        raise exceptions.NotAuthenticated("You must provide `?token=API_TOKEN` to use this service. Please check your emails to get this token.")

    # Grab the API key model, make sure it exists
    try:
        api_key = ApiKey.objects.get(key=key)
    except ApiKey.DoesNotExist:
        raise exceptions.AuthenticationFailed("This API token doesn't exist")

    package = get_object_or_404(Package, name=package_name)

    try:
        last_build = package.builds.get(build_number=build_number)
    except Build.DoesNotExist:
        raise exceptions.NotFound("Couldn't find a build for this package name")

    # Serialize the new build
    serializer = BuildSerializer(last_build)
    response_data = serializer.data.copy()
    response_data.update(last_build.extra)

    return Response(response_data)

class AccountView(APIView):

    def post(self, request, format=None):

        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        # Make sure no account exists with this email
        try:
            account = AccountEmail.objects.get(email=email)
            return Response({'error': "An account with the same email already exists. Please check your inbox to get your API token."}, status=status.HTTP_409_CONFLICT)
        except AccountEmail.DoesNotExist:
            pass

        # Create a new account
        account = Account()
        account.save()

        # Create a new email
        account_email = AccountEmail(account=account)
        account_email.email = email
        account_email.save()

        # Create a new API Key
        api_key = ApiKey(account=account)
        api_key.save()

        send_welcome_email(account, account_email, api_key)

        return Response({}, status=status.HTTP_201_CREATED)
