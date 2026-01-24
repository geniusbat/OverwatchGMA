from django.shortcuts import render, redirect

from . import models

# Create your views here.
def index(request,test_value=None):
    #Extract filtering parameters from url
    delegate_controls = models.delegate_controls.objects
    delegate_errors = models.delegate_errors.objects

    host = request.GET.get("host",None)
    if host != None:
        delegate_controls = delegate_controls.filter(host=host)
        delegate_errors = delegate_errors.filter(host=host)
    afterStamp = request.GET.get("afterStamp",None)
    if afterStamp != None:
        delegate_controls = delegate_controls.filter(timestamp__gt=afterStamp)
        delegate_errors = delegate_errors.filter(timestamp__gt=afterStamp)
    command = request.GET.get("command",None)
    if command != None:
        delegate_controls = delegate_controls.filter(command_name=command)
        delegate_errors = delegate_errors.filter(command_name=command)
    returncode = request.GET.get("returncode",None)
    if returncode != None:
        delegate_controls = delegate_controls.filter(returncode=returncode)
        delegate_errors = delegate_errors.filter(returncode=returncode)

    template = "index.html"
    context = {}
    #Add for how long the control has had the same output
    context["delegate_controls"] = delegate_controls.all()
    context["master_controls"] = models.master_controls.objects.all()
    context["delegate_errors"]  = delegate_errors.all()
    context["master_errors"]  = models.master_errors.objects.all()
    return render(request, template, context)

