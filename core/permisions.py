#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin


class IsAdmin(AccessMixin):
    """ Check is request user is Admin
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    def test_func(self, request):
        try:
            profile = request.user.profile
            result = True
        except Exception as exp:
            print(exp)
            result =  False
        finally:
            return result
       

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func(request)
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HasActiveProfile(AccessMixin):
    """ Check is request user has active profile
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    def test_func(self, request):
        try:
            profile = request.user.profile
            result = bool(profile and profile.active)
        except Exception as exp:
            print(exp)
            result =  False
        finally:
            return result
       

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func(request)
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HasActiveCompany(AccessMixin):
    """ Check is request user has active Company/Marchant
    Deny a request with a permission error if the test_func() method returns
    False.
    """
    def test_func(self, request):
        try:
            profile = request.user.profile
            result = bool(profile and profile.active and profile.company)
        except Exception as exp:
            print(exp)
            result = False
        finally:
            return result

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func(request)
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HasActiveCompanyBranch(AccessMixin):
    """ Check is request user has active Company/Marchant
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    def test_func(self, request):
        try:
            profile = request.user.profile
            result = bool(profile and profile.active and profile.company and profile.branch)
        except Exception as exp:
            print(exp)
            result = False
        finally:
            return result

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func(request)
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

def boot():
    pass

if __name__ == "__main__":
    boot()
