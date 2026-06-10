from django.core.management import call_command
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
import tempfile

from .admin import ContactMessageAdmin, SpecsRequestAdmin
from .models import (
    ContactInquiry,
    ContactMessage,
    HomePageContent,
    SiteSettings,
    Solution,
    SolutionVisual,
    SpecsRequest,
)
from .views import solution_detail


User = get_user_model()


class PhaseOneDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_initial_content", verbosity=0)

    def test_contact_get_returns_200(self):
        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_database_content(self):
        HomePageContent.objects.update_or_create(
            key="main",
            defaults={
                "browser_title": "Vanguard Home",
                "hero_title": "MISSION READY PLATFORM",
                "hero_description": "Editable home page text from the admin.",
                "cta_text": "VIEW SYSTEMS",
                "is_active": True,
            },
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "MISSION READY PLATFORM")
        self.assertContains(response, "Editable home page text from the admin.")
        self.assertContains(response, "VIEW SYSTEMS")

    def test_contact_post_saves_contact_inquiry(self):
        response = self.client.post(reverse("contact"), {
            "organization": "Falcon Ops",
            "name": "Nadia Samir",
            "email": "nadia@example.com",
            "phone": "01000000000",
            "message": "Please contact us about secure communications.",
        })

        self.assertRedirects(response, reverse("contact"))
        inquiry = ContactInquiry.objects.get()
        self.assertEqual(inquiry.inquiry_type, ContactInquiry.INQUIRY_CONTACT)
        self.assertEqual(inquiry.organization, "Falcon Ops")
        self.assertEqual(inquiry.source_path, reverse("contact"))

    def test_specs_post_saves_specs_inquiry_with_requested_solution(self):
        response = self.client.post(reverse("contact"), {
            "organization": "Falcon Ops",
            "name": "Nadia Samir",
            "email": "nadia@example.com",
            "phone": "01000000000",
            "message": "GET SPECS request for VULTURE UAVs",
            "inquiry_type": ContactInquiry.INQUIRY_SPECS,
            "requested_solution_slug": "vulture-uavs",
        })

        self.assertRedirects(response, reverse("contact"))
        inquiry = ContactInquiry.objects.get()
        self.assertEqual(inquiry.inquiry_type, ContactInquiry.INQUIRY_SPECS)
        self.assertEqual(inquiry.requested_solution_slug, "vulture-uavs")
        self.assertEqual(inquiry.requested_solution.slug, "vulture-uavs")

    def test_admin_proxy_querysets_split_contact_and_specs(self):
        solution = Solution.objects.get(slug="vulture-uavs")
        ContactInquiry.objects.create(
            organization="Falcon Ops",
            name="Contact Lead",
            email="contact@example.com",
            phone="01000000000",
            message="General contact message.",
            inquiry_type=ContactInquiry.INQUIRY_CONTACT,
        )
        ContactInquiry.objects.create(
            organization="Falcon Ops",
            name="Specs Lead",
            email="specs@example.com",
            phone="01000000001",
            message="GET SPECS request for VULTURE UAVs",
            inquiry_type=ContactInquiry.INQUIRY_SPECS,
            requested_solution=solution,
            requested_solution_slug=solution.slug,
        )

        request = RequestFactory().get("/admin/")
        site = AdminSite()

        contact_queryset = ContactMessageAdmin(
            ContactMessage,
            site,
        ).get_queryset(request)
        specs_queryset = SpecsRequestAdmin(
            SpecsRequest,
            site,
        ).get_queryset(request)

        self.assertEqual(list(contact_queryset.values_list("name", flat=True)), ["Contact Lead"])
        self.assertEqual(list(specs_queryset.values_list("name", flat=True)), ["Specs Lead"])

    def test_seed_is_idempotent(self):
        call_command("seed_initial_content", verbosity=0)

        self.assertEqual(Solution.objects.count(), 4)
        self.assertEqual(SolutionVisual.objects.count(), 12)

    def test_solution_routes_return_200_after_seed(self):
        route_names = [
            "vancom",
            "vulture_uavs",
            "skyguard",
            "tactical_data_link",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_unknown_solution_slug_redirects_to_solutions(self):
        request = RequestFactory().get("/solutions/unknown/")
        response = solution_detail(request, "unknown")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("solutions"))

    def test_inactive_solution_is_not_public(self):
        Solution.objects.filter(slug="skyguard").update(is_active=False)

        response = self.client.get(reverse("solutions"))
        self.assertNotIn(
            Solution.objects.get(slug="skyguard"),
            list(response.context["solutions"]),
        )

        request = RequestFactory().get("/solutions/skyguard/")
        detail_response = solution_detail(request, "skyguard")
        self.assertEqual(detail_response.status_code, 302)
        self.assertEqual(detail_response.url, reverse("solutions"))

    def test_solutions_page_uses_database_titles(self):
        Solution.objects.filter(slug="skyguard").update(title="SkyGuard Command")

        response = self.client.get(reverse("solutions"))

        self.assertContains(response, "SkyGuard")
        self.assertContains(response, "Command")

    def test_inactive_solution_is_removed_from_solution_map(self):
        Solution.objects.filter(slug="skyguard").update(is_active=False)

        response = self.client.get(reverse("solutions"))

        self.assertNotContains(response, "solution-link-skyguard")
        self.assertNotContains(response, "SkyGuard")


class PhaseTwoDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_initial_content", verbosity=0)
        cls.staff_user = User.objects.create_user(
            username="ops",
            password="secure-pass",
            is_staff=True,
        )
        cls.non_staff_user = User.objects.create_user(
            username="viewer",
            password="secure-pass",
            is_staff=False,
        )
        cls.solution = Solution.objects.get(slug="vulture-uavs")
        cls.inquiry = ContactInquiry.objects.create(
            organization="Falcon Ops",
            name="Nadia Samir",
            email="nadia@example.com",
            phone="01000000000",
            message="Please send specs.",
            inquiry_type=ContactInquiry.INQUIRY_SPECS,
            requested_solution=cls.solution,
            requested_solution_slug=cls.solution.slug,
            source_path="/contact/",
        )

    def test_anonymous_user_cannot_access_dashboard(self):
        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_non_staff_user_cannot_access_dashboard(self):
        self.client.login(username="viewer", password="secure-pass")

        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_staff_user_can_access_dashboard(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Operations Overview")

    def test_staff_user_can_access_home_content_dashboard(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:home_content"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home Page Content")

    def test_home_content_dashboard_updates_public_home(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:home_content"), {
            "browser_title": "Vanguard Updated",
            "hero_title": "UPDATED MISSION COPY",
            "hero_description": "Updated from the custom dashboard.",
        })

        self.assertRedirects(response, reverse("dashboard:home_content"))
        public_response = self.client.get(reverse("home"))
        self.assertContains(public_response, "UPDATED MISSION COPY")
        self.assertContains(public_response, "Updated from the custom dashboard.")

    def test_staff_user_can_access_reports_dashboard(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Operational Reports")
        self.assertContains(response, "Total inquiries")

    def test_staff_user_can_access_settings_dashboard(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:settings"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Site Settings")

    def test_settings_dashboard_updates_safe_fields(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:settings"), {
            "site_name": "Vanguard Command",
            "company_name": "Vanguard Technologies",
            "contact_email": "ops@example.com",
            "contact_phone": "+20 100 000 0000",
            "linkedin_url": "https://www.linkedin.com/company/vanguard",
            "footer_text": "Internal operations footer",
        })

        self.assertRedirects(response, reverse("dashboard:settings"))
        settings = SiteSettings.objects.get(key="main")
        self.assertEqual(settings.site_name, "Vanguard Command")
        self.assertEqual(settings.contact_email, "ops@example.com")
        self.assertTrue(settings.is_active)

    def test_settings_dashboard_rejects_invalid_email_and_url(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:settings"), {
            "site_name": "Vanguard Command",
            "company_name": "Vanguard Technologies",
            "contact_email": "not-an-email",
            "contact_phone": "+20 100 000 0000",
            "linkedin_url": "not-a-url",
            "footer_text": "Internal operations footer",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address")
        self.assertContains(response, "Enter a valid URL")

    def test_staff_user_can_access_users_dashboard(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:users"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Users Directory")
        self.assertContains(response, "ops")

    def test_users_dashboard_search_filters_users(self):
        User.objects.create_user(
            username="field-operator",
            email="field@example.com",
            password="secure-pass",
        )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:users"), {"q": "field"})

        self.assertContains(response, "field-operator")
        self.assertNotContains(response, "viewer")

    def test_users_dashboard_deactivates_regular_user(self):
        target = User.objects.create_user(
            username="regular-user",
            password="secure-pass",
        )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:users"), {
            "user_id": target.pk,
            "action": "deactivate",
        })

        self.assertRedirects(response, reverse("dashboard:users"))
        target.refresh_from_db()
        self.assertFalse(target.is_active)

    def test_users_dashboard_cannot_deactivate_self(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:users"), {
            "user_id": self.staff_user.pk,
            "action": "deactivate",
        })

        self.assertRedirects(response, reverse("dashboard:users"))
        self.staff_user.refresh_from_db()
        self.assertTrue(self.staff_user.is_active)

    def test_users_dashboard_cannot_deactivate_superuser(self):
        superuser = User.objects.create_superuser(
            username="root",
            email="root@example.com",
            password="secure-pass",
        )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:users"), {
            "user_id": superuser.pk,
            "action": "deactivate",
        })

        self.assertRedirects(response, reverse("dashboard:users"))
        superuser.refresh_from_db()
        self.assertTrue(superuser.is_active)

    def test_inquiries_page_displays_messages(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:inquiries"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nadia Samir")
        self.assertContains(response, "Falcon Ops")

    def test_inquiries_page_filters_by_status(self):
        ContactInquiry.objects.create(
            organization="Archived Org",
            name="Archived Lead",
            email="archived@example.com",
            phone="01000000001",
            message="Old message.",
            status=ContactInquiry.STATUS_ARCHIVED,
        )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(
            reverse("dashboard:inquiries"),
            {"status": ContactInquiry.STATUS_NEW},
        )

        self.assertContains(response, "Nadia Samir")
        self.assertNotContains(response, "Archived Lead")

    def test_inquiries_page_paginates_results(self):
        for index in range(30):
            ContactInquiry.objects.create(
                organization="Paged Org",
                name=f"Paged Lead {index}",
                email=f"paged{index}@example.com",
                phone="01000000001",
                message="Queued message.",
            )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(reverse("dashboard:inquiries"))

        self.assertEqual(response.context["inquiries"].paginator.per_page, 25)
        self.assertContains(response, "Page 1 of 2")

    def test_inquiries_solution_filter_matches_fallback_slug(self):
        ContactInquiry.objects.create(
            organization="Slug Org",
            name="Slug Only Lead",
            email="slug@example.com",
            phone="01000000002",
            message="Specs request saved with slug only.",
            inquiry_type=ContactInquiry.INQUIRY_SPECS,
            requested_solution_slug=self.solution.slug,
        )
        self.client.login(username="ops", password="secure-pass")

        response = self.client.get(
            reverse("dashboard:inquiries"),
            {"solution": self.solution.pk},
        )

        self.assertContains(response, "Slug Only Lead")

    def test_inquiry_status_can_be_changed_from_inbox(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:inquiries"), {
            "inquiry_id": self.inquiry.pk,
            "status": ContactInquiry.STATUS_CONTACTED,
        })

        self.assertRedirects(response, reverse("dashboard:inquiries"))
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, ContactInquiry.STATUS_CONTACTED)

    def test_inquiry_detail_updates_status_and_internal_notes(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:inquiry_detail", args=[self.inquiry.pk]),
            {
                "status": ContactInquiry.STATUS_REVIEWED,
                "internal_notes": "Follow up on Thursday.",
            },
        )

        self.assertRedirects(
            response,
            reverse("dashboard:inquiry_detail", args=[self.inquiry.pk]),
        )
        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, ContactInquiry.STATUS_REVIEWED)
        self.assertEqual(self.inquiry.internal_notes, "Follow up on Thursday.")

    def test_solution_edit_updates_content(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_edit", args=[self.solution.pk]),
            {
                "title": "VULTURE ISR Fleet",
                "subtitle": self.solution.subtitle,
                "description": "Updated operator-facing description.",
                "show_visual_nav": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:solutions"))
        self.solution.refresh_from_db()
        self.assertEqual(self.solution.title, "VULTURE ISR Fleet")
        self.assertEqual(self.solution.slug, "vulture-uavs")

    def test_solution_can_be_deactivated_from_dashboard_and_hidden_publicly(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(reverse("dashboard:solutions"), {
            "solution_id": self.solution.pk,
            "action": "deactivate",
        })

        self.assertRedirects(response, reverse("dashboard:solutions"))
        self.solution.refresh_from_db()
        self.assertFalse(self.solution.is_active)
        public_response = self.client.get(reverse("vulture_uavs"))
        self.assertRedirects(public_response, reverse("solutions"))

    def test_solution_edit_saves_without_primary_image(self):
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_edit", args=[self.solution.pk]),
            {
                "title": self.solution.title,
                "subtitle": self.solution.subtitle,
                "description": self.solution.description,
                "show_visual_nav": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard:solutions"))

    def test_solution_edit_uploads_primary_image(self):
        self.client.login(username="ops", password="secure-pass")
        image = SimpleUploadedFile(
            "primary.png",
            b"primary-image-content",
            content_type="image/png",
        )

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("dashboard:solution_edit", args=[self.solution.pk]),
                    {
                        "title": self.solution.title,
                        "subtitle": self.solution.subtitle,
                        "description": self.solution.description,
                        "show_visual_nav": "on",
                        "primary_image": image,
                    },
                )

        self.assertRedirects(response, reverse("dashboard:solutions"))
        self.solution.refresh_from_db()
        self.assertTrue(self.solution.primary_image.name.endswith("primary.png"))
        self.assertEqual(self.solution.primary_image_path, "")

    def test_visuals_management_updates_existing_visual(self):
        visual = self.solution.visuals.first()
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_edit", args=[self.solution.pk]),
            {
                "intent": "gallery_update",
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "1",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-id": visual.pk,
                "form-0-title": "Updated visual",
            },
        )

        self.assertRedirects(
            response,
            reverse("dashboard:solution_edit", args=[self.solution.pk]),
        )
        visual.refresh_from_db()
        self.assertEqual(visual.title, "Updated visual")
        self.assertEqual(visual.caption, "Updated visual")

    def test_gallery_ajax_reorders_visuals(self):
        first, second = list(self.solution.visuals.all()[:2])
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_gallery_reorder", args=[self.solution.pk]),
            {"visual_ids[]": [second.pk, first.pk]},
        )

        self.assertEqual(response.status_code, 200)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(second.sort_order, 10)
        self.assertEqual(first.sort_order, 20)

    def test_gallery_ajax_deletes_visual(self):
        visual = self.solution.visuals.first()
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_gallery_delete", args=[self.solution.pk, visual.pk]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(SolutionVisual.objects.filter(pk=visual.pk).exists())

    def test_gallery_ajax_replaces_visual_image(self):
        visual = self.solution.visuals.first()
        self.client.login(username="ops", password="secure-pass")
        image = SimpleUploadedFile(
            "replacement.png",
            b"replacement-image",
            content_type="image/png",
        )

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("dashboard:solution_gallery_replace", args=[self.solution.pk, visual.pk]),
                    {"image": image},
                )

        self.assertEqual(response.status_code, 200)
        visual.refresh_from_db()
        self.assertEqual(visual.image_path, "")
        self.assertIn("replacement", visual.uploaded_image.name)

    def test_gallery_ajax_updates_visual_title(self):
        visual = self.solution.visuals.first()
        self.client.login(username="ops", password="secure-pass")

        response = self.client.post(
            reverse("dashboard:solution_gallery_title", args=[self.solution.pk, visual.pk]),
            {"title": "Updated AJAX title"},
        )

        self.assertEqual(response.status_code, 200)
        visual.refresh_from_db()
        self.assertEqual(visual.title, "Updated AJAX title")
        self.assertEqual(visual.caption, "Updated AJAX title")

    def test_gallery_ajax_uploads_image(self):
        self.client.login(username="ops", password="secure-pass")
        image = SimpleUploadedFile(
            "payload.png",
            b"not-a-real-png-but-valid-upload-by-content-type",
            content_type="image/png",
        )

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("dashboard:solution_gallery_upload", args=[self.solution.pk]),
                    {"images": image},
                )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            SolutionVisual.objects.filter(
                solution=self.solution,
                title="Payload",
                uploaded_image__contains="payload",
            ).exists()
        )

    def test_gallery_ajax_rejects_non_image_upload(self):
        self.client.login(username="ops", password="secure-pass")
        document = SimpleUploadedFile(
            "payload.txt",
            b"plain text",
            content_type="text/plain",
        )

        response = self.client.post(
            reverse("dashboard:solution_gallery_upload", args=[self.solution.pk]),
            {"images": document},
        )

        self.assertEqual(response.status_code, 400)

    def test_gallery_ajax_rejects_unsupported_jpg(self):
        # اختبار إن الـ AJAX بيترفض لو الملف JPEG/JPG
        self.client.login(username="ops", password="secure-pass")
        image = SimpleUploadedFile(
            "payload.jpg",
            b"fake-jpeg",
            content_type="image/jpeg",
        )
        response = self.client.post(
            reverse("dashboard:solution_gallery_upload", args=[self.solution.pk]),
            {"images": image},
        )
        self.assertEqual(response.status_code, 400)

    def test_gallery_ajax_accepts_glb_and_webp(self):
        # اختبار إن الـ AJAX بيقبل ملفات glb و webp
        self.client.login(username="ops", password="secure-pass")
        glb = SimpleUploadedFile(
            "model.glb",
            b"fake-glb",
            content_type="model/gltf-binary",
        )
        webp = SimpleUploadedFile(
            "image.webp",
            b"fake-webp",
            content_type="image/webp",
        )
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("dashboard:solution_gallery_upload", args=[self.solution.pk]),
                    {"images": [glb, webp]},
                )
        self.assertEqual(response.status_code, 200)

    def test_solution_form_rejects_unsupported_logo(self):
        # اختبار إن الفورم بترفض اللوجو لو امتداده مش مسموح بيه
        self.client.login(username="ops", password="secure-pass")
        bad_image = SimpleUploadedFile(
            "logo.gif",
            b"fake-gif",
            content_type="image/gif",
        )
        response = self.client.post(
            reverse("dashboard:solution_edit", args=[self.solution.pk]),
            {
                "title": self.solution.title,
                "subtitle": self.solution.subtitle,
                "description": self.solution.description,
                "logo_image": bad_image,
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("logo_image", form.errors)
        self.assertEqual(form.errors["logo_image"], ["Only webp, png, and glb files are allowed."])
