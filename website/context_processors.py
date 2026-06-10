from django.contrib.staticfiles.storage import staticfiles_storage
from .models import SiteSettings


def site_settings(request):
    """
    Context processor لإضافة إعدادات الموقع (اللوجو والـ Favicon) لكل صفحة
    """
    settings = SiteSettings.objects.filter(key="main", is_active=True).first()
    
    if not settings:
        return {
            "site_settings": None,
            "site_logo_url": staticfiles_storage.url("website/images/Icon.png"),
            "site_favicon_url": staticfiles_storage.url("website/images/Icon.png"),
        }

    logo_url = ""
    if settings.logo:
        logo_url = settings.logo.url
    elif settings.logo_path:
        logo_url = staticfiles_storage.url(settings.logo_path)

    favicon_url = ""
    if settings.favicon:
        favicon_url = settings.favicon.url
    elif settings.favicon_path:
        favicon_url = staticfiles_storage.url(settings.favicon_path)

    return {
        "site_settings": settings,
        "site_logo_url": logo_url,
        "site_favicon_url": favicon_url,
    }
