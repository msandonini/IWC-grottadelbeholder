import codecs
import json
import mimetypes
import os.path

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage


from django.views import View

from ProgettoIWC import settings
from .models import User, Admin
from .forms import *

import hashlib




