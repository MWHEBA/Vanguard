from django.db import models


class HomePageContent(models.Model):
    key = models.SlugField(max_length=40, unique=True, default="main")
    browser_title = models.CharField(
        max_length=120,
        default="Trusted Defense Solutions",
    )
    hero_title = models.CharField(max_length=180)
    hero_description = models.TextField()
    cta_text = models.CharField(max_length=40, default="OUR SOLUTIONS")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "home page content"
        verbose_name_plural = "home page content"

    def __str__(self):
        return "Home page content"


class SiteSettings(models.Model):
    key = models.SlugField(max_length=40, unique=True, default="main")
    site_name = models.CharField(max_length=120, default="Vanguard Technologies")
    company_name = models.CharField(max_length=120, default="Vanguard Technologies")
    contact_email = models.EmailField(default="info@vanguard.example")
    contact_phone = models.CharField(max_length=40, blank=True)
    linkedin_url = models.URLField(blank=True)
    footer_text = models.CharField(
        max_length=160,
        default="ALL RIGHTS RESERVED 2026 (C) VANGUARD TECHNOLOGIES",
    )
    logo_path = models.CharField(max_length=255, blank=True)
    logo = models.FileField(upload_to="site-branding/", blank=True)
    favicon_path = models.CharField(max_length=255, blank=True)
    favicon = models.FileField(upload_to="site-branding/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return self.site_name


class Solution(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    subtitle = models.CharField(max_length=160, blank=True)
    description = models.TextField()
    cta_text = models.CharField(max_length=40, default="GET SPECS")
    solution_id = models.CharField(
        max_length=80,
        unique=True,
        help_text="Used by templates and CSS. Change carefully after publishing.",
    )
    illustration_type = models.CharField(max_length=80, blank=True)
    primary_image_path = models.CharField(max_length=255, blank=True)
    primary_image = models.FileField(upload_to="solution-primary/", blank=True)
    logo_image_path = models.CharField(max_length=255, blank=True)
    logo_image = models.FileField(upload_to="solution-logo/", blank=True)
    visual_caption = models.CharField(max_length=120, blank=True)
    show_visual_nav = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class SolutionVisual(models.Model):
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        related_name="visuals",
    )
    title = models.CharField(max_length=120)
    caption = models.CharField(max_length=160, blank=True)
    image_path = models.CharField(max_length=255, blank=True)
    uploaded_image = models.FileField(upload_to="solution-gallery/", blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return f"{self.solution.title}: {self.title}"


class ContactInquiry(models.Model):
    INQUIRY_CONTACT = "contact"
    INQUIRY_SPECS = "specs"
    INQUIRY_TYPE_CHOICES = [
        (INQUIRY_CONTACT, "Contact"),
        (INQUIRY_SPECS, "Specs"),
    ]

    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_CONTACTED = "contacted"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    organization = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    message = models.TextField()
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPE_CHOICES,
        default=INQUIRY_CONTACT,
    )
    requested_solution = models.ForeignKey(
        Solution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries",
    )
    requested_solution_slug = models.SlugField(max_length=120, blank=True)
    source_path = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "contact inquiries"

    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()}"


class ContactMessage(ContactInquiry):
    class Meta:
        proxy = True
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"


class SpecsRequest(ContactInquiry):
    class Meta:
        proxy = True
        verbose_name = "specs request"
        verbose_name_plural = "specs requests"
