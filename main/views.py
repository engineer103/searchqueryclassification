from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import os.path

# Create your views here.
def get_media(request, p):
    f=os.path.join(settings.MEDIA_ROOT, p)
    return HttpResponse(open(f,'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
