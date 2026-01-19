from rest_framework import serializers

from . import models

class storeMixing():
    def store(self, validated_data):
        ins = models.delegate_controls(
                host = validated_data["host"],
                timestamp = validated_data["timestamp"],
                command_name = validated_data["command_name"],
                returncode = validated_data["returncode"],
                message = validated_data["message"],
                last_change = validated_data["timestamp"]
        )
        return ins.store()

class delegate_controlsFullSerializer(serializers.ModelSerializer, storeMixing):
    class Meta:
        model = models.delegate_controls
        fields = ["pk","host", "timestamp", "command_name", "returncode", "message", "previous_timestamp", "previous_returncode", "previous_message", "last_change"]
    
    def create(self, validated_data):
        return self.store(validated_data)

class delegate_controlsSimpleSerializer(serializers.ModelSerializer, storeMixing):
    class Meta:
        model = models.delegate_controls
        fields = ["host", "timestamp", "command_name", "returncode", "message"]

    def create(self, validated_data):
        return self.store(validated_data)

class delegate_errorsSerializer(serializers.ModelSerializer, storeMixing):
    class Meta:
        model = models.delegate_errors
        fields = ["pk","host", "timestamp", "command_name", "returncode", "message"]