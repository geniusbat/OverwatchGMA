from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status, generics
from .permissions import HostRegistryValidIpPermissions,ApiViewPermission
import datetime

from main import models, serializers

#delegate_controls views
class delegate_controlsList(generics.ListCreateAPIView):
    queryset = models.delegate_controls.objects.all()
    permission_classes = [HostRegistryValidIpPermissions,ApiViewPermission]
    requires_permission_to = ["main.delegate_controls"] #Define here what models have to be checked of permissions (as permissions are not automatically checked in api views)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.delegate_controlsSimpleSerializer
        return serializers.delegate_controlsFullSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=isinstance(request.data,list))
        if serializer.is_valid():
            #Save controls passed in post
            ins = serializer.create(serializer.data)
            #If a single instance just add it to a list so it is iterable by the following code
            if not type(ins) is list:
                ins = [ins]
            #Now update host_registry with the ip of the request
            seen_hosts = [] #Keep alreay seen hosts to not run the same code multiple times
            new_ip = request.META["REMOTE_ADDR"]
            #Get ip from X-Forwarded-For, if not just keep it from request
            if "HTTP_X_FORWARDED_FOR" in request.META.keys():
                new_ip = request.META["HTTP_X_FORWARDED_FOR"]
            for element in ins:
                if not element.host in seen_hosts:
                    registry = models.hosts_registry.objects.get(host = element.host)
                    #Update registry with new ip and also check for any incongruences
                    valid_entry = registry.check_update_entry(new_ip, datetime.datetime.now(datetime.UTC).timestamp())
                    valid_entry = "" if valid_entry else " (ip incongruency)"
                    seen_hosts.append(element.host)
            return Response("Created successfully{}: {}".format(valid_entry,str(ins)), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class delegate_controlsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.delegate_controls.objects.all()
    permission_classes = [HostRegistryValidIpPermissions,ApiViewPermission]
    requires_permission_to = ["main.delegate_controls"] 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.delegate_controlsSimpleSerializer
        return serializers.delegate_controlsFullSerializer

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response("Deleted successfully", status=status.HTTP_200_OK)

#delegate_errors views
class delegate_errorsList(generics.ListCreateAPIView):
    queryset = models.delegate_errors.objects.all()
    permission_classes = [HostRegistryValidIpPermissions,ApiViewPermission]
    requires_permission_to = ["main.delegate_errors"]

    def get_serializer_class(self):
        return serializers.delegate_errorsSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=isinstance(request.data,list))
        if serializer.is_valid():
            #Save controls passed in post
            ins = serializer.create(serializer.data)
            #If a single instance just add it to a list so it is iterable by the following code
            if not type(ins) is list:
                ins = [ins]
            return Response("Created successfully: {}".format(str(ins)), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class delegate_errorsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.delegate_errors.objects.all()
    permission_classes = [HostRegistryValidIpPermissions,ApiViewPermission]
    requires_permission_to = ["main.delegate_errors"]

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response("Deleted successfully", status=status.HTTP_200_OK)