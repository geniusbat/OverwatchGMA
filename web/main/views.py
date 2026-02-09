from django.shortcuts import render, redirect
import datetime

from . import models

# Create your views here.
def index(request):
    #Extract filtering parameters from url
    delegate_controls = models.delegate_controls.objects
    delegate_errors = models.delegate_errors.objects


    host = request.GET.get("host","")
    if host != "":
        delegate_controls = delegate_controls.filter(host=host)
        delegate_errors = delegate_errors.filter(host=host)
    afterStamp = request.GET.get("afterStamp","")
    if afterStamp != "":
        delegate_controls = delegate_controls.filter(timestamp__gt=afterStamp)
        delegate_errors = delegate_errors.filter(timestamp__gt=afterStamp)
    command = request.GET.get("command","")
    if command != "":
        delegate_controls = delegate_controls.filter(command_name=command)
        delegate_errors = delegate_errors.filter(command_name=command)
    returncode = request.GET.get("returncode","")
    if returncode != "":
        delegate_controls = delegate_controls.filter(returncode=returncode)
        delegate_errors = delegate_errors.filter(returncode=returncode)

    now = datetime.datetime.now(datetime.UTC)
    last_options = [
        [int((now-datetime.timedelta(minutes=5)).timestamp()), "5 minutes"],
        [int((now-datetime.timedelta(minutes=30)).timestamp()), "30 minutes"],
        [int((now-datetime.timedelta(hours=1)).timestamp()), "1 hour"],
        [int((now-datetime.timedelta(hours=2)).timestamp()), "2 hours"],
        [int((now-datetime.timedelta(hours=7)).timestamp()), "7 hours"],
        [int((now-datetime.timedelta(days=1)).timestamp()), "1 day"],
        [int((now-datetime.timedelta(days=15)).timestamp()), "15 days"]
    ]

    template = "index.html"
    context = {}
    #Add for how long the control has had the same output
    context["delegate_controls"] = delegate_controls.all()
    context["master_controls"] = models.master_controls.objects.all()
    context["delegate_errors"]  = delegate_errors.all()
    context["master_errors"]  = models.master_errors.objects.all()
    context["hosts"] = models.hosts_registry.objects.all()
    context["last_options"] = last_options

    return render(request, template, context)


def dashboard(request):
    template = "dashboard.html"
    context = {}
    context["hosts"] = models.hosts_registry.objects.all()
    context["statuses"] = models.hosts_registry.objects.get_statuses()
    context["messages_count"] = models.hosts_registry.objects.get_host_messages_count()
    context["recent_errors"] = list(models.delegate_controls.objects.get_erroring_controls()[:5]) + list(models.master_errors.objects.all()[:5]) + list(models.delegate_errors.objects.all()[:5])
    return render(request, template, context)

def master(request):
    now = datetime.datetime.now(datetime.UTC)
    last_options = [
        [int((now-datetime.timedelta(minutes=5)).timestamp()), "5 minutes"],
        [int((now-datetime.timedelta(minutes=30)).timestamp()), "30 minutes"],
        [int((now-datetime.timedelta(hours=1)).timestamp()), "1 hour"],
        [int((now-datetime.timedelta(hours=2)).timestamp()), "2 hours"],
        [int((now-datetime.timedelta(hours=7)).timestamp()), "7 hours"],
        [int((now-datetime.timedelta(days=1)).timestamp()), "1 day"],
        [int((now-datetime.timedelta(days=15)).timestamp()), "15 days"]
    ]

    template = "master_view.html"
    context = {}
    context["master_controls"] = models.master_controls.objects.all()
    context["master_errors"]  = models.master_errors.objects.all()
    context["last_options"] = last_options
    return render(request, template, context)