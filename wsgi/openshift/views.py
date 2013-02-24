import os
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def home(request):
    form = UploadFileForm()
    return render_to_response('home/home.html', {'form': form})

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    return HttpResponseRedirect('/')


