from rest_framework.permissions import BasePermission
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.utils.serializer_helpers import ReturnList
import datetime

from web.authentication import DelegateAnonymousUser
from main.models import hosts_registry, master_errors

class HostRegistryValidIpPermissions(BasePermission):
    """
    This class handles so that the source ip of the action is contemplated inside the allowed_ips for a host in host_registry
    """
    message = 'Ip not found in hosts_registry or no valid entry to begin with'
    #This permission class checks the "valid_ips" field for the given host and return true if the ip of the request is in it
    def _check_ip_is_valid(self, host:str, ip:str)->bool:
        entry = None
        #Make sure entry exists
        try:
            entry = hosts_registry.objects.get(host=host)
        except hosts_registry.DoesNotExist as e:
            master_errors.objects.create(
                host = host,
                timestamp = datetime.datetime.now(datetime.UTC).timestamp(),
                command_name = "No host_registry entry for given host: {}".format(host),
                returncode = 1,
                message = "No host_registry entry for given host: {}".format(host)
            )
            return False
        #Continue, check ip is inside valid ips (which is a string)
        return ip in entry.valid_ips

    def _extract_hostNip(self,request,view) -> list[tuple[str,str]]:
        #Get request
        serializer = view.get_serializer(data=request.data,many=isinstance(request.data,list))
        if serializer.is_valid():
            data = serializer.data
            #Get ip
            ip = request.META["REMOTE_ADDR"]
            #Get ip from X-Forwarded-For, if not just keep it from request
            if "HTTP_X_FORWARDED_FOR" in request.META.keys():
                ip = request.META["HTTP_X_FORWARDED_FOR"]
            result = []
            #As we allow the creation of multiple instances at the same time, we have to make sure all of them are allowed
            if type(data) is ReturnList or type(data) is list:
                for element in data:
                    result.append((element["host"], ip))
            #Only one instance, add it to list
            else:
                result.append((data["host"], ip))
            return result    
        #Serialization went wrong      
        else:
            raise ValidationError(serializer.errors)


    def has_permission(self, request, view)->bool:
        #Return true to options request if user is authenticated (this means we allow this action to all users)
        if request.user and request.user.is_authenticated:
            if request.method == "OPTIONS":
                return True
        #Return true if user is a staff member
        if request.user.is_staff or request.user.is_admin:
            return True
        pairs = self._extract_hostNip(request, view)
        #Iterate over all pairs and check permissions, if anything fails return False, if everything goes well return true
        for pair in pairs:
            if not self._check_ip_is_valid(pair[0],pair[1]):
                return False
        return True

    def has_object_permission(self, request, view, obj)->bool:
        return self.has_permission(request, view)


class ApiViewPermission(BasePermission):
    """
    This permissions class requires that the ApiView class has a property 'requires_permission_to:list' 
    Defining the models that should be checked if the user has permissions
    This class handles permissions both for DelegateTokens (where user is DelegateAnonymousUser) and for DRF Tokens associated with a django user.
    """
    message = "User hasn't got necessary permission"
    permission_map = {
        "GET": "{app_label}.view_{model_name}",
        "POST": "{app_label}.add_{model_name}",
        "PUT": "{app_label}.change_{model_name}",
        "PATCH": "{app_label}.change_{model_name}",
        "DELETE": "{app_label}.delete_{model_name}",
    }

    allowed_delegate_user_actions = {
        #"GET": ["main.delegate_controls","main.delegate_errors"],
        "POST": ["main.delegate_controls","main.delegate_errors"]
    }

    def _get_permission(self, method, permision):
        app, model = permision.split(".")
        if method not in self.permission_map:
            raise MethodNotAllowed(method)
        perm = self.permission_map.get(method).format(app_label=app, model_name=model)
        return perm

    def _has_permission_delegate(self, method, permision):
        if method in self.allowed_delegate_user_actions:
            if permision in self.allowed_delegate_user_actions[method]:
                return True
            else:
                return False
        else:
            raise MethodNotAllowed(method)

    def has_permission(self, request, view)->bool:
        #Return true to options request if user is authenticated (this means we allow this action to all users)
        if request.user and request.user.is_authenticated:
            if request.method == "OPTIONS":
                return True
        #Handle permissions if user is a DelegateAnonymousUser
        if hasattr(request.user,"is_delegate"):
            required_permissions = view.requires_permission_to
            perms = []
            for permission in required_permissions:
                perms.append(self._has_permission_delegate(method=request.method, permision=permission))
            if all(perms):
                return True
            return False
        
        #Continue for other normal users
        required_permissions = view.requires_permission_to
        perms = []
        for permission in required_permissions:
            perms.append(request.user.has_perm(self._get_permission(method=request.method, permision=permission)))
        if all(perms):
            return True
        return False
