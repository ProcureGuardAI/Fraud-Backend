from django.apps import AppConfig
from django.conf import settings
import os
import joblib

class TestmodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testmodel'
