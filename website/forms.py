from django import forms

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
