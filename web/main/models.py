from django.db import models
import datetime


def _aux_get_now_utc_timestamp():
    return datetime.datetime.now(datetime.UTC).timestamp()

class delegate_controls(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()
    previous_timestamp = models.IntegerField(blank=True,null=True,default=None)
    previous_returncode = models.IntegerField(blank=True,null=True,default=None)
    previous_message = models.TextField(blank=True,null=True,default=None)
    last_change = models.IntegerField(blank=True,null=True,default=None)

    class Meta:
        db_table = "delegate_controls"
        ordering = ["-timestamp","host", "command_name"]
        verbose_name = "delegate_control"
        verbose_name_plural = "delegate_controls"

    def store(self):
        #Control already existed, update
        try:
            previous_control = delegate_controls.objects.get(host=self.host,command_name=self.command_name)
            #Assign current values to previous 
            previous_control.timestamp = self.timestamp
            previous_control.previous_message = previous_control.message
            previous_control.previous_returncode = previous_control.returncode
            previous_control.previous_timestamp = previous_control.timestamp
            #If return code or message changed set last_change to now
            if previous_control.message != self.message or previous_control.returncode  != self.returncode:
                previous_control.last_change = _aux_get_now_utc_timestamp()
            #Assign new values
            previous_control.message = self.message
            previous_control.returncode = self.returncode
            previous_control.timestamp = self.timestamp
            previous_control.save()
            return previous_control
        #Control did not exist, create
        except delegate_controls.DoesNotExist:
            obj = delegate_controls(
                host = self.host,
                timestamp = self.timestamp,
                command_name = self.command_name,
                returncode = self.returncode,
                message = self.message,
                last_change = _aux_get_now_utc_timestamp()
            )
            obj.save()
            return obj
    
    def __str__(self):
        return "{}-{} ({}):{}".format(self.host, self.command_name, self.timestamp, self.returncode)


class delegate_errors(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    class Meta:
        db_table = "delegate_errors"
        ordering = ["-timestamp","host", "command_name"]
        verbose_name = "delegate_error"
        verbose_name_plural = "delegate_errors"

    def __str__(self):
        return "{}-{} ({}):{}".format(self.host, self.command_name, self.timestamp, self.returncode)


class master_controls(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()
    previous_timestamp = models.IntegerField(blank=True,null=True,default=None)
    previous_returncode = models.IntegerField(blank=True,null=True,default=None)
    previous_message = models.TextField(blank=True,null=True,default=None)
    last_change = models.IntegerField(blank=True,null=True,default=None)

    class Meta:
        db_table = "master_controls"
        ordering = ["-timestamp","host", "command_name"]
        verbose_name = "master_control"
        verbose_name_plural = "master_controls"

    def store(self):
        #Control already existed, update
        try:
            previous_control = delegate_controls.objects.get(host=self.host,command_name=self.command_name)
            #Assign current values to previous 
            previous_control.timestamp = self.timestamp
            previous_control.previous_message = previous_control.message
            previous_control.previous_returncode = previous_control.returncode
            previous_control.previous_timestamp = previous_control.timestamp
            #If return code or message changed set last_change to now
            if previous_control.message != self.message or previous_control.returncode  != self.returncode:
                previous_control.last_change = _aux_get_now_utc_timestamp()
            #Assign new values
            previous_control.message = self.message
            previous_control.returncode = self.returncode
            previous_control.timestamp = self.timestamp
            previous_control.save()
            return previous_control
        #Control did not exist, create
        except delegate_controls.DoesNotExist:
            obj = delegate_controls(
                host = self.host,
                timestamp = self.timestamp,
                command_name = self.command_name,
                returncode = self.returncode,
                message = self.message,
                last_change = _aux_get_now_utc_timestamp()
            )
            obj.save()
            return obj

    def __str__(self):
        return "{}-{} ({}):{}".format(self.host, self.command_name, self.timestamp, self.returncode)

class master_errors(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    class Meta:
        db_table = "master_errors"
        ordering = ["-timestamp","host", "command_name"]
        verbose_name = "master_error"
        verbose_name_plural = "master_errors"

    def __str__(self):
        return "{}-{} ({}):{}".format(self.host, self.command_name, self.timestamp, self.returncode)

class hosts_registry(models.Model):
    host = models.CharField(max_length=16, unique=True)
    ip = models.CharField(max_length=39)
    valid_ips = models.CharField(max_length=130, default="127.0.0.1") #String made up of ips, separated by commas
    previous_ip = models.CharField(max_length=39, blank=True, null=True)
    last_updated = models.IntegerField(blank=True, default=_aux_get_now_utc_timestamp)
    previous_last_updated = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "hosts_registry"
        ordering = ["-last_updated","host"]
        verbose_name = "host_registry"
        verbose_name_plural = "hosts_registry"

    def check_update_entry(self, new_ip:str, new_stamp:int):
        aux = self.simply_check_validity(new_ip, new_stamp)
        self.update_entry(new_ip, new_stamp)
        return aux

    def simply_check_validity(self, new_ip:str, new_stamp:int):
        if self.previous_ip != None and self.previous_ip != new_ip:
            master_errors.objects.create(
                host = self.host,
                timestamp = datetime.datetime.now(datetime.UTC).timestamp(),
                command_name = "Ip incongruences in host_registry",
                returncode = 1,
                message = "Ip incogruence for host {}, went from {} to {}".format(self.host, self.previous_ip, new_ip)
            )
            return False
        else:
            return True

    def update_entry(self, new_ip:str, new_stamp:int):
        self.previous_ip = self.ip
        self.previous_last_updated = self.last_updated
        self.ip = new_ip
        self.last_updated = new_stamp
        self.save()
        

    def __str__(self):
        return "{}: {}<--{} ({})".format(self.host, self.ip, self.previous_ip, self.last_updated)