from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def admin_test(request):
    return render(request, 'admin/test.html')