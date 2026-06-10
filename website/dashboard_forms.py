from django import forms
from django.contrib.staticfiles import finders

from .models import (
    ContactInquiry,
    HomePageContent,
    SiteSettings,
    Solution,
    SolutionVisual,
)


class RichTextWidget(forms.Textarea):
    """Custom textarea widget for rich text editing"""

    def __init__(self, attrs=None, max_chars=None):
        if attrs is None:
            attrs = {}
        attrs["data-rich-editor"] = "true"
        if max_chars:
            attrs["data-max-chars"] = str(max_chars)
        self.max_chars = max_chars
        super().__init__(attrs)


class DashboardFormMixin:
    def apply_dashboard_classes(self):
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            current_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{current_class} dashboard-input".strip()


class InquiryStatusForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ("status",)


class InquiryDetailForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ("status", "internal_notes")
        widgets = {
            "internal_notes": forms.Textarea(attrs={"rows": 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()


class HomePageContentDashboardForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = (
            "browser_title",
            "hero_title",
            "hero_description",
        )
        widgets = {
            "hero_description": RichTextWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_active = True
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class SiteSettingsDashboardForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "site_name",
            "company_name",
            "contact_email",
            "contact_phone",
            "linkedin_url",
            "footer_text",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_active = True
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class SolutionDashboardForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Solution
        fields = (
            "title",
            "subtitle",
            "description",
            "logo_image",
            "primary_image",
            "show_visual_nav",
        )
        widgets = {
            "description": RichTextWidget(),
            "logo_image": forms.ClearableFileInput(attrs={
                "id": "logo-image-input",
                "data-logo-image-input": "",
            }),
            "primary_image": forms.ClearableFileInput(attrs={
                "id": "primary-image-input",
                "data-primary-image-input": "",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()

    def clean_logo_image(self):
        # الدالة دي بتتحقق إن اللوجو المرفوع امتداده مسموح بيه (webp أو png أو glb) بس
        logo_image = self.cleaned_data.get("logo_image")
        if logo_image:
            ext = logo_image.name.split(".")[-1].lower() if "." in logo_image.name else ""
            if ext not in {"webp", "png", "glb"}:
                raise forms.ValidationError("Only webp, png, and glb files are allowed.")
        return logo_image

    def clean_primary_image(self):
        # الدالة دي بتتحقق إن الصورة الرئيسية المرفوعة امتدادها مسموح بيه (webp أو png أو glb) بس
        primary_image = self.cleaned_data.get("primary_image")
        if primary_image:
            ext = primary_image.name.split(".")[-1].lower() if "." in primary_image.name else ""
            if ext not in {"webp", "png", "glb"}:
                raise forms.ValidationError("Only webp, png, and glb files are allowed.")
        return primary_image

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("logo_image"):
            instance.logo_image_path = ""
        if self.cleaned_data.get("primary_image"):
            instance.primary_image_path = ""
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class SolutionVisualForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = SolutionVisual
        fields = ("title",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.caption = instance.title
        if commit:
            instance.save()
            self.save_m2m()
        return instance


SolutionVisualFormSet = forms.modelformset_factory(
    SolutionVisual,
    form=SolutionVisualForm,
    extra=0,
    can_delete=False,
)


class SiteBrandingDashboardForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "logo",
            "favicon",
        )
        widgets = {
            "logo": forms.ClearableFileInput(attrs={
                "id": "logo-branding-input",
                "name": "logo",
                "type": "file",
                "accept": ".webp,.png,.ico,.svg,image/webp,image/png,image/svg+xml",
                "hidden": "true",
                "data-logo-branding-input": "",
            }),
            "favicon": forms.ClearableFileInput(attrs={
                "id": "favicon-branding-input",
                "name": "favicon",
                "type": "file",
                "accept": ".ico,.png,.svg,image/png,image/svg+xml,image/x-icon",
                "hidden": "true",
                "data-favicon-branding-input": "",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_dashboard_classes()

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            ext = logo.name.split(".")[-1].lower() if "." in logo.name else ""
            if ext not in {"webp", "png", "ico", "svg"}:
                raise forms.ValidationError("Only webp, png, ico, and svg files are allowed for logo.")
        return logo

    def clean_favicon(self):
        favicon = self.cleaned_data.get("favicon")
        if favicon:
            ext = favicon.name.split(".")[-1].lower() if "." in favicon.name else ""
            if ext not in {"ico", "png", "svg"}:
                raise forms.ValidationError("Only ico, png, and svg files are allowed for favicon.")
        return favicon

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("logo"):
            instance.logo_path = ""
        if self.cleaned_data.get("favicon"):
            instance.favicon_path = ""
        if commit:
            instance.save()
            self.save_m2m()
        return instance
