#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = 'https://ahmadabdulnasir.com.ng'
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"


from rest_framework import serializers

class CustomeSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source="user.username", read_only=True)

    def get_created_by(self, obj):
        if hasattr(obj, "created_by"):
            return obj.created_by.username


    def get_timestamp(self, obj):
        return f"{obj.timestamp:%Y-%m-%d %H:%M:%S %p}"

    def get_updated(self, obj):
        return f"{obj.updated:%Y-%m-%d %H:%M:%S %p}"
