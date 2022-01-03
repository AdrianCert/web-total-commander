"""The module keeps the configuration for django registration"""
from django.apps import AppConfig


class TotalcmdConfig(AppConfig):
    """Application configuration class"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'totalcmd'
