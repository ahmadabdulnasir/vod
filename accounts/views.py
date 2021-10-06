from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import  UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from core.permisions import HasActiveProfile, HasActiveCompany, HasActiveCompanyBranch

# from pos.models import Product
# from pos.forms import ProductForm

# Create your views here.

# General Views
class UserLoginView(View):
    """ Allows login of User"""
    template_name = "accounts/login.html"
    context = {}

    def post(self, *args, **kwargs):
        context = {}
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            # Redirect to a success page.
            msg = "Login Success!!!"
            print(msg)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                message=msg,
                # extra_tags="text-success bg-warning",
            )
            token, created = Token.objects.get_or_create(user=user)
            return HttpResponseRedirect(reverse("accounts:dashboard"))
        msg = "Invalid Username and/or Password, Please Check and Try Again !!!"
        messages.add_message(
            self.request,
            messages.ERROR,
            message=msg,
            # extra_tags="text-danger bg-warning",
        )
        return render(self.request, template_name=self.template_name, context=context)

    def get(self, *args, **kwargs):
        self.context["extra_body_class"] = "login-page"
        return render(
            self.request, template_name=self.template_name, context=self.context
        )


class DashboardView(LoginRequiredMixin, View):
    """ Allows managing of account dashboard and redirect to the appropiate dashboard"""

    def get(self, *args, **kwargs):
        context = {}
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            profile = False
        if profile and profile.user_type == "agent":
            return HttpResponseRedirect(reverse("accounts:agent-dashboard"))
        elif profile and profile.user_type == "staff":
            return HttpResponseRedirect(reverse("accounts:staff-dashboard"))
        elif profile and profile.user_type == "admin":
            return HttpResponseRedirect(reverse("accounts:staff-dashboard"))
            # return HttpResponseRedirect(reverse("admin:index"))
        else:
            #TODO: redirect to permission Page
            return HttpResponseRedirect(reverse("accounts:edit-profile"))



# ./General Views


# Staff/Cachier Views
class StaffDashboardView(LoginRequiredMixin, HasActiveCompanyBranch, View):
    """ Allows managing of account for Staff"""

    template_name = "dashboard/staffs/staff_dashboard.html"

    def get(self, *args, **kwargs):
        context = {}
        today = timezone.now()
        user = self.request.user
        profile = user.profile
        # company = profile.company
        # branch = profile.branch

        products_num = 12 #Product.objects.filter(company=company, branch=branch).count()
        sales_num = 1782
        sales_revenue = 9017726
        context["products_num"] = products_num
        context["sales_num"] = sales_num
        context["sales_revenue"] = sales_revenue
        

        return render(
            request=self.request, template_name=self.template_name, context=context
        )
