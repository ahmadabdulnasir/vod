from rest_framework import serializers
from locations.models import State, LGA


class StateModelSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = [
            "pk",
            "title",
            "State_ID",
            "state_code",
            "zone",
            "zone_code",
            "created",
            "updated",
        ]

    def get_created(self, obj):
        return f"{obj.updated: '%Y-%m-%d %H:%M:%S %p'}"

    def get_updated(self, obj):
        return f"{obj.updated: '%Y-%m-%d %H:%M:%S %p'}"


class LGAModelSerializer(serializers.ModelSerializer):
    state_title = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = LGA
        fields = ["pk", "title", "LGA_ID", "state", "state_title", "created", "updated"]

    def get_created(self, obj):
        return f"{obj.updated: '%Y-%m-%d %H:%M:%S %p'}"

    def get_updated(self, obj):
        return f"{obj.updated: '%Y-%m-%d %H:%M:%S %p'}"

    def get_state_title(self, obj):
        return f"{obj.state.title}"
