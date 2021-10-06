from django.views.generic import ListView, DetailView, View
from .utils import Egg
from .models import MainPage, HomePageSlider, SiteInformation
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from blog.models import Post
from .forms import SiteInformationEditAddForm

# Create your views here.


class HomeView(View):
    def get(self, *args, **kwargs):
        context = {}
        template_name = "core/home.html"
        posts = (
            Post.objects.all()
            .filter(status="publish", post_type="post")
            .order_by("-updated")[:6]
        )
        # lessons = Post.objects.all().filter(publish=True, post_type='knowledge').order_by('-pub_time')[:3]
        context["posts"] = posts
        # context['lessons'] = lessons
        try:
            slider = HomePageSlider.objects.filter(active=True).first()
            context["slider"] = slider
        except HomePageSlider.DoesNotExit as exp:
            print("[Error]: ", exp)
        finally:
            return render(self.request, template_name=template_name, context=context)


class MainPageDetailView(DetailView):
    template_name = "core/pages.html"
    model = MainPage
    query_pk_and_slug = True
    context_object_name = "page"
    # context = {}
    def get_context_data(self, *args, **kwargs):
        try:
            context = super(MainPageDetailView, self).get_context_data(*args, **kwargs)
            print("Found")
            return context
        except MainPage.DoesNotExist:
            context["page"] = Egg
            # TODO: send mail on error
            print("Not Found")
            return context
        return context


def contactView(request):
    next_url = reverse("audience:contact")
    return HttpResponseRedirect(next_url)


class SettingsListView(View):
    """ List Core Settings, staff view"""
    template_name = "accounts/dashboard/core/core_settings_list.html"

    def get(self, *args, **kwargs):
        context = {}
        all_site_informations = SiteInformation.objects.all()
        try:
            context["settings"] = all_site_informations
        except SiteInformation.DoesNotExist as exp:
            msg = f"Error while Saving!!! Error: {exp}"
            self.messages.add_message(
                self.request, self.messages.ERROR, message=msg, extra_tags="text-danger"
            )
            context["slider_form"]

        finally:
            context["title"] = "Core Settings"
            return render(self.request, template_name=self.template_name, context=context)


class SettingsEditAddView(View):
    """ Allow Editing/Adding of Core Settings, staff view"""
    template_name = "accounts/dashboard/academics/class_list.html"
    def get(self, *args, **kwargs):
        context = {}
        all_site_informations = SiteInformation.objects.all()
        try:
            slider = all_site_informations.filter(uid=class_uid)
            slider_form = SiteInformationEditAddForm(instance=class_)
            context["slider_form"] = slider_form
        except SiteInformation.DoesNotExist as exp:
            slider_form = SiteInformationEditAddForm()
            context["slider_form"]

        finally:
            return render(self.request, template_name=self.template_name, context=context)
