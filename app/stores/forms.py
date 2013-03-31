from django import forms
from extra_views import InlineFormSet
from epiceditor.widgets import EpicEditorWidget
from .models import ClaimRequest, Store, Address


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        if hasattr(self.Meta, 'classes'):
            for field, css in self.Meta.classes.items():
                if field in self.fields:
                    self.fields[field].widget.attrs['class'] = css


class ClaimRequestForm(BootstrapModelForm):

    def __init__(self, *args, **kwargs):
        super(ClaimRequestForm, self).__init__(*args, **kwargs)
        for field, css in self.Meta.classes.items():
            if field in self.fields:
                self.fields[field].widget.attrs['class'] = css

    class Meta:
        model = ClaimRequest
        fields = ('note',)
        classes = {
            'note': 'input-xxlarge',
        }


class StoreForm(BootstrapModelForm):

    class Meta:
        model = Store
        exclude = ('slug', 'address', 'chain', 'editor')
        classes = {
            'name': 'input-xxlarge',
            'long_description': 'input-xxlarge',
        }
        widgets = {
            'long_description': EpicEditorWidget(attrs={'rows': 40}, themes={'editor':'epic-light.css'})
        }


class AddressForm(BootstrapModelForm):

    class Meta:
        model = Address
        exclude = ('name', 'geo_latitude', 'geo_longitude')


class AddressInline(InlineFormSet):
    model = Address
