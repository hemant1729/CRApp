from django.shortcuts import render
from django.http import HttpResponse
from .accounts.views import *
from .admin.views import *
from .student.views import *

# Create your views here.
def index(request):
    return HttpResponse("HELLO WORLD!!!")