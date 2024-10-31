from django.apps import AppConfig
from django.conf import settings
import os
import joblib

class TestmodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testmodel'
    MODEL_FILE = os.path.join(settings.MODELS, 'model.pkl')
    model = joblib.load(MODEL_FILE)

    