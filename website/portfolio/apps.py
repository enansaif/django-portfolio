"""
    Configuration file for the Portfolio app.
    """
from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """
    Configuration class for the Portfolio app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "portfolio"
