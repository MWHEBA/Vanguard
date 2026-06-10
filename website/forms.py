from django import forms

from .models import ContactInquiry

# فورم التواصل للعملاء والشركات المهتمة
class ContactForm(forms.Form):
    organization = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-input'
        })
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': '',
            'class': 'form-input'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-input-phone'
        })
    )
    message = forms.CharField(
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter Message',
            'class': 'form-textarea',
            'rows': 6
        })
    )
    inquiry_type = forms.ChoiceField(
        choices=ContactInquiry.INQUIRY_TYPE_CHOICES,
        required=False,
        widget=forms.HiddenInput()
    )
    requested_solution_slug = forms.SlugField(
        max_length=120,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_inquiry_type(self):
        return self.cleaned_data.get("inquiry_type") or ContactInquiry.INQUIRY_CONTACT
