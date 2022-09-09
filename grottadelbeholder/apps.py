import os
import shutil
from datetime import datetime

from django.apps import AppConfig

from ProgettoIWC import settings
from ProgettoIWC.mylib.mediaThreading import MyTimer


class GrottadelbeholderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grottadelbeholder'

    def ready(self):
        print("Server started - Cleaning media:", datetime.now())
        deleteMedia()
        timer = MyTimer(86400, deleteMedia, bVerbose=True)
        timer.start_timer()


def deleteMedia():
    if os.path.exists(settings.MEDIA_ROOT):
        shutil.rmtree(settings.MEDIA_ROOT)
