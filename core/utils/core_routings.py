#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
from django.contrib.auth.models import User
from accounts.models import UserProfile
import re

def getDeletedUser():
    user, created = User.objects.get_or_create(username='deleted_user')
    return user


def getSystemUser():
    user, created = User.objects.get_or_create(username='System')
    return user


def getDeletedUserProfile():
    try:
       profile = UserProfile.objects.get(user__username='deleted_user')
    except UserProfile.DoesNotExist as exp:
        user = getDeletedUser()
        profile = UserProfile(user=user, staff_id="deleted_user")
        profile.save()
    return profile

def validateAccountNumber(num):
    """ takes account number and validate if it's avalid account format Params:	num: string of account number"""
    try:
        if re.match("^[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{4}-[0-9]{2}$", num):
            return True
        else:
            return False
    except Exception:
        return False
        
def boot():
    pass

if __name__ == "__main__":
    boot()
