"""
Configuration file for the Authenticator app.
"""
from django.apps import AppConfig


class AuthenticatorConfig(AppConfig):
    """
    Configuration class for the Authenticator app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authenticator'
