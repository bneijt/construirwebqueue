import os
import random
import re
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django import forms
from django.template import RequestContext
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

newJobPattern = re.compile("_i([0-9]+)\\.tar\\.xz")
doneJobPattern = re.compile("_d([0-9]+)\\.tar\\.xz")

def doneJobName(filename):
    global doneJobPattern
    return doneJobPattern.search(filename) != None

def newJobName(filename):
    global newJobPattern
    return newJobPattern.search(filename) != None

class UploadFileForm(forms.Form):
    file = forms.FileField(max_length = 50)
    def clean_file(self):
        f = self.cleaned_data['file']
        if f.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Uploads may not be larger then %i bytes" % settings.MAX_UPLOAD_SIZE)
        if not f.name.endswith(".tar.xz"):
            raise forms.ValidationError("Only .tar.xz files are accepted")
        if ".." in f.name:
            raise forms.ValidationError("File names may not contain two dots")
        return f


def handle_uploaded_file(f):
    storageDirectory = None
    if newJobName(f.name):
        storageDirectory = settings.QUEUE_DIRECTORY
    elif doneJobName(f.name):
        storageDirectory = settings.DONE_DIRECTORY
    if storageDirectory == None:
        return HttpResponseServerError("Internal server error")
    storageFileName = os.path.join(storageDirectory, f.name)
    with open(storageFileName, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return HttpResponseRedirect('/thank you')

def home(request):
    doneList = os.listdir(settings.DONE_DIRECTORY)
    queueList = os.listdir(settings.QUEUE_DIRECTORY)
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            if doneJobName(f.name):
                if len(doneList) > settings.QUEUE_SIZE:
                    return HttpResponseServerError("Done full")
            if newJobName(f.name):
                if len(queueList) > settings.QUEUE_SIZE:
                    return HttpResponseServerError("Queue full")
            return handle_uploaded_file(f)
    return render_to_response(
            'home/home.html',
            {"form": form, "queueList": queueList, "doneList": doneList}, 
            context_instance=RequestContext(request))


def done(request, filename):
    print(filename)
    #Pop a random task from the queue
    doneList = os.listdir(settings.DONE_DIRECTORY)
    if not filename in doneList:
        raise Http404
    path = os.path.join(settings.DONE_DIRECTORY, filename)
    print(path)
    wrapper = FileWrapper(open(path, "r"))
    response = HttpResponse(wrapper, content_type = "application/octet-stream")
    response["Content-Length"] = os.path.getsize(path)
    return response

#def download(request):
#    #Pop a random task from the queue
#    queueList = os.listdir(settings.QUEUE_DIRECTORY)
#    filename = os.path.join(settings.QUEUE_DIRECTORY, random.sample(queueList, 1))
#    wrapper = FileWrapper(open(filename))
#    response = HttpResponse(wrapper, content_type = "application/octet-stream")
#    response["Content-Length"] = os.path.getsize(filename)
#    return response




