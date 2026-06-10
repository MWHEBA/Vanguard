from django.contrib import admin

from .models import (
    ContactInquiry,
    ContactMessage,
    HomePageContent,
    SiteSettings,
    Solution,
    SolutionVisual,
    SpecsRequest,
)


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ("key", "browser_title", "is_active", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": (
                "key",
                "browser_title",
                "hero_title",
                "hero_description",
                "cta_text",
                "is_active",
            )
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "site_name", "company_name", "contact_email", "is_active", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": (
                "key",
                "site_name",
                "company_name",
                "contact_email",
                "contact_phone",
                "linkedin_url",
                "footer_text",
                "is_active",
            )
        }),
        ("Branding", {
            "fields": (
                "logo_path",
                "logo",
                "favicon_path",
                "favicon",
            )
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


class SolutionVisualInline(admin.TabularInline):
    model = SolutionVisual
    extra = 0
    fields = ("title", "caption", "image_path", "uploaded_image", "sort_order", "is_active")
    ordering = ("sort_order", "title")


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "solution_id",
        "is_active",
        "sort_order",
        "updated_at",
    )
    search_fields = ("title", "subtitle", "description", "slug")
    list_filter = ("is_active", "show_visual_nav")
    ordering = ("sort_order", "title")
    inlines = (SolutionVisualInline,)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": (
                "title",
                "slug",
                "subtitle",
                "description",
                "cta_text",
                "is_active",
                "sort_order",
            )
        }),
        ("Template and visual behavior", {
            "description": "slug and solution_id are sensitive public/template identifiers. Change carefully after publishing.",
            "fields": (
                "solution_id",
                "illustration_type",
                "logo_image_path",
                "logo_image",
                "primary_image_path",
                "primary_image",
                "visual_caption",
                "show_visual_nav",
            ),
        }),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


class InquiryAdminBase(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "email",
        "inquiry_type",
        "requested_solution",
        "status",
        "created_at",
    )
    search_fields = ("name", "organization", "email", "phone", "message")
    list_filter = ("inquiry_type", "status", "requested_solution", "created_at")
    readonly_fields = ("created_at", "updated_at", "source_path")
    actions = ("mark_as_reviewed", "mark_as_contacted", "archive")

    @admin.action(description="Mark selected inquiries as reviewed")
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_REVIEWED)

    @admin.action(description="Mark selected inquiries as contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_CONTACTED)

    @admin.action(description="Archive selected inquiries")
    def archive(self, request, queryset):
        queryset.update(status=ContactInquiry.STATUS_ARCHIVED)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(InquiryAdminBase):
    pass


@admin.register(ContactMessage)
class ContactMessageAdmin(InquiryAdminBase):
    list_filter = ("status", "created_at")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            inquiry_type=ContactInquiry.INQUIRY_CONTACT
        )


@admin.register(SpecsRequest)
class SpecsRequestAdmin(InquiryAdminBase):
    list_display = (
        "name",
        "organization",
        "email",
        "requested_solution",
        "status",
        "created_at",
    )
    list_filter = ("status", "requested_solution", "created_at")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            inquiry_type=ContactInquiry.INQUIRY_SPECS
        )
