from django.db import models

#TODO: Just get "latest" result of each control for each host

class delegate_controls(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    #Not properly working, maybe just add 2 rows to the table to handle this (instead of rechecking DB)
    @property
    def time_running(self) -> int:
        return 100
        #Get controls of the same command and host, the third filter is to make sure no "future" controls are used (as they would return negative time. Take note that the filter will include the control itself running the method
        controls = delegate_controls.objects.filter(host=self.host).filter(command_name=self.command_name).filter(timestamp__lte=self.timestamp).order_by("-timestamp")
        difference = 0
        #Iterate over all controls and get the first one to not be of the same returncode, the difference between times is how long the control has had that given output
        for control in controls:
            if control.returncode == self.returncode:
                difference = self.timestamp - control.timestamp
            else:
                break
        return difference

    class Meta:
        db_table = "delegate_controls"


class delegate_errors(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    class Meta:
        db_table = "delegate_errors"


class master_controls(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    class Meta:
        db_table = "master_controls"

class master_errors(models.Model):
    host = models.CharField(max_length=16)
    timestamp = models.IntegerField()
    command_name = models.CharField(max_length=25)
    returncode = models.IntegerField()
    message = models.TextField()

    class Meta:
        db_table = "master_errors"


class hosts_registry(models.Model):
    host = models.CharField(max_length=16)
    ip = models.CharField(max_length=39)
    previous_ip = models.CharField(max_length=39)
    last_updated = models.IntegerField()
    previous_last_updated = models.IntegerField()

    class Meta:
        db_table = "hosts_registry"