from django import forms
from .models import SiteInformation


class SiteInformationEditAddForm(forms.ModelForm):
    class Meta:
        model = SiteInformation
        fields = "__all__"
        # exclude = ('ref_id', 'updated', 'active')
