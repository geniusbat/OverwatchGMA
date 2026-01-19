from django.shortcuts import render, redirect

from . import models

# Create your views here.
def index(request):
    template = "index.html"
    context = {}
    delegate_controls = models.delegate_controls.objects.all().order_by("host","command_name")
    #Add for how long the control has had the same output
    context["delegate_controls"] = delegate_controls.values()
    return render(request, template, context)