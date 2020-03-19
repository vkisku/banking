import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
from accounts.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
#from accounts.models import profile_extension
import datetime
from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.core.mail import EmailMessage
from django.core.mail import send_mail, get_connection
from django.core.cache import cache

@login_required
def home(request):
    return HttpResponse("<h1>Home</h1>")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def user_from_session_key(session_key):
    """
    Returns the User related to the given Django session key.
    """
    from django.conf import settings
    from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
    from django.contrib.auth.models import AnonymousUser

    session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    session_wrapper = session_engine.SessionStore(session_key)
    session = session_wrapper.load()
    user_id = session.get(SESSION_KEY)
    backend_id = session.get(BACKEND_SESSION_KEY)

    if user_id and backend_id:
        auth_backend = load_backend(backend_id)
        user = auth_backend.get_user(user_id)

        if user:
            return user

    return AnonymousUser()
