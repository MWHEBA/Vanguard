from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from functools import wraps

from .dashboard_forms import (
    HomePageContentDashboardForm,
    InquiryDetailForm,
    InquiryStatusForm,
    SiteSettingsDashboardForm,
    SiteBrandingDashboardForm,
    SolutionDashboardForm,
    SolutionVisualFormSet,
)
from .models import ContactInquiry, HomePageContent, SiteSettings, Solution, SolutionVisual


User = get_user_model()

def is_allowed_file(filename):
    # الدالة دي بتتأكد إن امتداد الملف مسموح بيه (webp أو png أو glb بس)
    if not filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in {"webp", "png", "glb"}


def staff_json_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_active or not request.user.is_staff:
            return JsonResponse({"error": "Staff authentication required."}, status=403)
        try:
            return view_func(request, *args, **kwargs)
        except Exception as exc:
            # Convert Http404 (and similar) into JSON so frontend receives predictable responses.
            from django.http import Http404

            if isinstance(exc, Http404):
                return JsonResponse({"error": "No resource with given identifier found."}, status=404)
            raise

    return wrapper


@staff_member_required
def index(request):
    latest_inquiries = (
        ContactInquiry.objects
        .select_related("requested_solution")
        .order_by("-created_at")[:5]
    )
    metrics = {
        "new_inquiries": ContactInquiry.objects.filter(
            status=ContactInquiry.STATUS_NEW,
        ).count(),
        "new_specs": ContactInquiry.objects.filter(
            inquiry_type=ContactInquiry.INQUIRY_SPECS,
            status=ContactInquiry.STATUS_NEW,
        ).count(),
        "contacted": ContactInquiry.objects.filter(
            status=ContactInquiry.STATUS_CONTACTED,
        ).count(),
        "active_solutions": Solution.objects.filter(is_active=True).count(),
    }

    return render(request, "dashboard/index.html", {
        "current_dashboard_page": "overview",
        "latest_inquiries": latest_inquiries,
        "metrics": metrics,
    })


@staff_member_required
def inquiries(request):
    if request.method == "POST":
        inquiry = get_object_or_404(ContactInquiry, pk=request.POST.get("inquiry_id"))
        form = InquiryStatusForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "Inquiry status updated.")
        else:
            messages.error(request, "Could not update inquiry status.")
        return redirect("dashboard:inquiries")

    queryset = ContactInquiry.objects.select_related("requested_solution")
    search_query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    inquiry_type = request.GET.get("type", "").strip()
    solution_id = request.GET.get("solution", "").strip()

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query)
            | Q(organization__icontains=search_query)
            | Q(email__icontains=search_query)
        )
    if status:
        queryset = queryset.filter(status=status)
    if inquiry_type:
        queryset = queryset.filter(inquiry_type=inquiry_type)
    if solution_id:
        selected_solution = Solution.objects.filter(pk=solution_id).first()
        if selected_solution:
            queryset = queryset.filter(
                Q(requested_solution_id=selected_solution.pk)
                | Q(requested_solution_slug=selected_solution.slug)
            )
        else:
            queryset = queryset.none()

    paginator = Paginator(queryset, 25)
    inquiries_page = paginator.get_page(request.GET.get("page"))

    tabs = [
        ("all", "All", reverse_query_url("dashboard:inquiries")),
        ("new", "New", reverse_query_url("dashboard:inquiries", status=ContactInquiry.STATUS_NEW)),
        ("specs", "Specs", reverse_query_url("dashboard:inquiries", type=ContactInquiry.INQUIRY_SPECS)),
        ("contacted", "Contacted", reverse_query_url("dashboard:inquiries", status=ContactInquiry.STATUS_CONTACTED)),
        ("archived", "Archived", reverse_query_url("dashboard:inquiries", status=ContactInquiry.STATUS_ARCHIVED)),
    ]
    active_tab = "all"
    if status == ContactInquiry.STATUS_NEW:
        active_tab = "new"
    elif inquiry_type == ContactInquiry.INQUIRY_SPECS:
        active_tab = "specs"
    elif status == ContactInquiry.STATUS_CONTACTED:
        active_tab = "contacted"
    elif status == ContactInquiry.STATUS_ARCHIVED:
        active_tab = "archived"

    return render(request, "dashboard/inquiries.html", {
        "current_dashboard_page": "inquiries",
        "active_tab": active_tab,
        "inquiries": inquiries_page,
        "inquiry_type_choices": ContactInquiry.INQUIRY_TYPE_CHOICES,
        "solutions": Solution.objects.all(),
        "status_choices": ContactInquiry.STATUS_CHOICES,
        "tabs": tabs,
        "filters": {
            "q": search_query,
            "status": status,
            "type": inquiry_type,
            "solution": solution_id,
        },
    })


@staff_member_required
def home_content(request):
    content, _ = HomePageContent.objects.get_or_create(
        key="main",
        defaults={
            "browser_title": "Trusted Defense Solutions",
            "hero_title": "TRUSTED SOLUTIONS\nENGINEERED FOR MISSION SUCCESS.",
            "hero_description": (
                "Vanguard Technologies is an advanced defense technology company "
                "delivering integrated, smart, reliable, scalable mission-critical "
                "security special solutions."
            ),
            "cta_text": "OUR SOLUTIONS",
            "is_active": True,
        },
    )

    if request.method == "POST":
        form = HomePageContentDashboardForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Home page content updated.")
            return redirect("dashboard:home_content")
        messages.error(request, "Review the highlighted home page fields.")
    else:
        form = HomePageContentDashboardForm(instance=content)

    return render(request, "dashboard/home_content.html", {
        "content_object": content,
        "current_dashboard_page": "home",
        "form": form,
    })


@staff_member_required
def inquiry_detail(request, pk):
    inquiry = get_object_or_404(
        ContactInquiry.objects.select_related("requested_solution"),
        pk=pk,
    )
    if request.method == "POST":
        form = InquiryDetailForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "Inquiry updated.")
            return redirect("dashboard:inquiry_detail", pk=inquiry.pk)
        messages.error(request, "Review the highlighted inquiry fields.")
    else:
        form = InquiryDetailForm(instance=inquiry)

    return render(request, "dashboard/inquiry_detail.html", {
        "current_dashboard_page": "inquiries",
        "form": form,
        "inquiry": inquiry,
    })


@staff_member_required
def reports(request):
    now = timezone.now()
    seven_days_ago = now - timezone.timedelta(days=7)
    inquiries = ContactInquiry.objects.select_related("requested_solution")

    status_counts = {
        item["status"]: item["total"]
        for item in inquiries.values("status").annotate(total=Count("id"))
    }
    type_counts = {
        item["inquiry_type"]: item["total"]
        for item in inquiries.values("inquiry_type").annotate(total=Count("id"))
    }
    solution_rows = (
        inquiries
        .filter(requested_solution__isnull=False)
        .values("requested_solution__title")
        .annotate(total=Count("id"))
        .order_by("-total", "requested_solution__title")
    )

    total_inquiries = inquiries.count()
    metrics = {
        "total_inquiries": total_inquiries,
        "last_7_days": inquiries.filter(created_at__gte=seven_days_ago).count(),
        "contact": type_counts.get(ContactInquiry.INQUIRY_CONTACT, 0),
        "specs": type_counts.get(ContactInquiry.INQUIRY_SPECS, 0),
        "active_solutions": Solution.objects.filter(is_active=True).count(),
        "inactive_solutions": Solution.objects.filter(is_active=False).count(),
    }

    status_rows = [
        {
            "label": label,
            "status": value,
            "total": status_counts.get(value, 0),
            "percent": percentage(status_counts.get(value, 0), total_inquiries),
        }
        for value, label in ContactInquiry.STATUS_CHOICES
    ]
    type_rows = [
        {
            "label": label,
            "type": value,
            "total": type_counts.get(value, 0),
            "percent": percentage(type_counts.get(value, 0), total_inquiries),
        }
        for value, label in ContactInquiry.INQUIRY_TYPE_CHOICES
    ]

    return render(request, "dashboard/reports.html", {
        "current_dashboard_page": "reports",
        "metrics": metrics,
        "solution_rows": solution_rows,
        "status_rows": status_rows,
        "type_rows": type_rows,
    })


@staff_member_required
def settings(request):
    site_settings, _ = SiteSettings.objects.get_or_create(
        key="main",
        defaults={
            "site_name": "Vanguard Technologies",
            "company_name": "Vanguard Technologies",
            "contact_email": "info@vanguard.example",
            "footer_text": "ALL RIGHTS RESERVED 2026 (C) VANGUARD TECHNOLOGIES",
            "is_active": True,
        },
    )

    if request.method == "POST":
        form = SiteSettingsDashboardForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated.")
            return redirect("dashboard:settings")
        messages.error(request, "Review the highlighted settings fields.")
    else:
        form = SiteSettingsDashboardForm(instance=site_settings)

    return render(request, "dashboard/settings.html", {
        "current_dashboard_page": "settings",
        "form": form,
        "settings_object": site_settings,
    })


@staff_member_required
def branding(request):
    site_settings, _ = SiteSettings.objects.get_or_create(
        key="main",
        defaults={
            "site_name": "Vanguard Technologies",
            "company_name": "Vanguard Technologies",
            "contact_email": "info@vanguard.example",
            "footer_text": "ALL RIGHTS RESERVED 2026 (C) VANGUARD TECHNOLOGIES",
            "is_active": True,
        },
    )

    if request.method == "POST":
        form = SiteBrandingDashboardForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site branding updated.")
            return redirect("dashboard:branding")
        messages.error(request, "Review the highlighted branding fields.")
    else:
        form = SiteBrandingDashboardForm(instance=site_settings)

    # احسب URLs للصور الحالية
    logo_url = ""
    if site_settings.logo:
        logo_url = site_settings.logo.url
    elif site_settings.logo_path:
        logo_url = staticfiles_storage.url(site_settings.logo_path)

    favicon_url = ""
    if site_settings.favicon:
        favicon_url = site_settings.favicon.url
    elif site_settings.favicon_path:
        favicon_url = staticfiles_storage.url(site_settings.favicon_path)

    return render(request, "dashboard/branding.html", {
        "current_dashboard_page": "branding",
        "form": form,
        "settings_object": site_settings,
        "logo_url": logo_url,
        "favicon_url": favicon_url,
    })


@staff_member_required
def solutions(request):
    if request.method == "POST":
        solution = get_object_or_404(Solution, pk=request.POST.get("solution_id"))
        solution.is_active = request.POST.get("action") == "activate"
        solution.save(update_fields=["is_active", "updated_at"])
        messages.success(request, f"{solution.title} status updated.")
        return redirect("dashboard:solutions")

    solution_rows = (
        Solution.objects
        .prefetch_related("visuals")
        .annotate(visual_count=Count("visuals"))
        .order_by("sort_order", "title")
    )
    return render(request, "dashboard/solutions.html", {
        "current_dashboard_page": "solutions",
        "solutions": solution_rows,
    })


@staff_member_required
def users(request):
    if request.method == "POST":
        target_user = get_object_or_404(User, pk=request.POST.get("user_id"))
        action = request.POST.get("action")

        if target_user.pk == request.user.pk:
            messages.error(request, "You cannot change your own account status from this dashboard.")
        elif target_user.is_superuser:
            messages.error(request, "Superuser accounts must be managed from Django Admin.")
        elif action in {"activate", "deactivate"}:
            target_user.is_active = action == "activate"
            target_user.save(update_fields=["is_active"])
            messages.success(request, f"{target_user.username} status updated.")
        else:
            messages.error(request, "Unsupported user action.")
        return redirect("dashboard:users")

    queryset = User.objects.all().order_by("username")
    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    if search_query:
        queryset = queryset.filter(
            Q(username__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )
    if status_filter == "active":
        queryset = queryset.filter(is_active=True)
    elif status_filter == "inactive":
        queryset = queryset.filter(is_active=False)
    elif status_filter == "staff":
        queryset = queryset.filter(is_staff=True)

    metrics = {
        "total": User.objects.count(),
        "active": User.objects.filter(is_active=True).count(),
        "staff": User.objects.filter(is_staff=True).count(),
        "inactive": User.objects.filter(is_active=False).count(),
    }

    paginator = Paginator(queryset, 25)
    users_page = paginator.get_page(request.GET.get("page"))

    return render(request, "dashboard/users.html", {
        "current_dashboard_page": "users",
        "filters": {
            "q": search_query,
            "status": status_filter,
        },
        "metrics": metrics,
        "users": users_page,
    })


def reverse_query_url(route_name, **params):
    from django.urls import reverse

    url = reverse(route_name)
    if not params:
        return url

    query = "&".join(
        f"{key}={value}"
        for key, value in params.items()
        if value
    )
    return f"{url}?{query}"


def percentage(value, total):
    if not total:
        return 0
    return round((value / total) * 100)


@staff_member_required
def solution_edit(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    visuals_queryset = solution.visuals.all()

    if request.method == "POST":
        intent = request.POST.get("intent", "solution")
        if intent == "gallery_update":
            form = SolutionDashboardForm(instance=solution)
            formset = SolutionVisualFormSet(request.POST, queryset=visuals_queryset)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Gallery updated.")
                return redirect("dashboard:solution_edit", pk=solution.pk)
            messages.error(request, "Review the highlighted gallery fields.")
        else:
            form = SolutionDashboardForm(request.POST, request.FILES, instance=solution)
            formset = SolutionVisualFormSet(queryset=visuals_queryset)
            if form.is_valid():
                form.save()
                messages.success(request, "Solution updated.")
                return redirect("dashboard:solutions")
            messages.error(request, "Review the highlighted solution fields.")
    else:
        form = SolutionDashboardForm(instance=solution)
        formset = SolutionVisualFormSet(queryset=visuals_queryset)

    return render(request, "dashboard/solution_form.html", {
        "current_dashboard_page": "solutions",
        "form": form,
        "formset": formset,
        "solution": solution,
    })


@staff_json_required
def solution_gallery_upload(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)

    uploaded_files = request.FILES.getlist("images")
    if not uploaded_files:
        return JsonResponse({"error": "No images were uploaded."}, status=400)

    current_max_order = (
        solution.visuals
        .order_by("-sort_order")
        .values_list("sort_order", flat=True)
        .first()
    ) or 0
    created_items = []
    errors = []

    for index, uploaded_file in enumerate(uploaded_files, start=1):
        # هنتحقق من كل ملف مرفوع لو امتداده مش مسموح بيه هنضيف رسالة تحذير
        if not is_allowed_file(uploaded_file.name):
            errors.append(f"{uploaded_file.name}: Only webp, png, and glb files are allowed.")
            continue

        title = readable_filename(uploaded_file.name)
        visual = SolutionVisual.objects.create(
            solution=solution,
            title=title,
            caption=title,
            uploaded_image=uploaded_file,
            sort_order=current_max_order + (index * 10),
            is_active=True,
        )
        created_items.append(serialize_gallery_item(visual))

    if not created_items and errors:
        return JsonResponse({"error": " ".join(errors)}, status=400)

    return JsonResponse({
        "items": created_items,
        "errors": errors,
    })


@staff_json_required
def solution_gallery_reorder(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)

    visual_ids = request.POST.getlist("visual_ids[]") or request.POST.getlist("visual_ids")
    if not visual_ids:
        return JsonResponse({"error": "No gallery order was provided."}, status=400)

    visuals = {
        str(visual.pk): visual
        for visual in solution.visuals.filter(pk__in=visual_ids)
    }
    for index, visual_id in enumerate(visual_ids, start=1):
        visual = visuals.get(str(visual_id))
        if visual:
            visual.sort_order = index * 10
            visual.save(update_fields=["sort_order", "updated_at"])

    return JsonResponse({"ok": True})


@staff_json_required
def solution_gallery_replace(request, pk, visual_pk):
    visual = get_object_or_404(SolutionVisual, pk=visual_pk, solution_id=pk)
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)

    uploaded_file = request.FILES.get("image")
    if not uploaded_file:
        return JsonResponse({"error": "No replacement image was uploaded."}, status=400)
    # هنتأكد إن ملف الاستبدال الجديد امتداده صح
    if not is_allowed_file(uploaded_file.name):
        return JsonResponse({"error": "Only webp, png, and glb files are allowed."}, status=400)

    visual.uploaded_image = uploaded_file
    visual.image_path = ""
    visual.save(update_fields=["uploaded_image", "image_path", "updated_at"])
    return JsonResponse(serialize_gallery_item(visual))


@staff_json_required
def solution_gallery_title(request, pk, visual_pk):
    visual = get_object_or_404(SolutionVisual, pk=visual_pk, solution_id=pk)
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)

    title = request.POST.get("title", "").strip()
    if not title:
        return JsonResponse({"error": "Title is required."}, status=400)

    visual.title = title
    visual.caption = title
    visual.save(update_fields=["title", "caption", "updated_at"])
    return JsonResponse(serialize_gallery_item(visual))


@staff_json_required
def solution_gallery_delete(request, pk, visual_pk):
    visual = get_object_or_404(SolutionVisual, pk=visual_pk, solution_id=pk)
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=405)

    visual.delete()
    return JsonResponse({"ok": True, "id": visual_pk})


def readable_filename(filename):
    name = filename.rsplit(".", 1)[0]
    return name.replace("-", " ").replace("_", " ").strip().title() or "Gallery Image"


def serialize_gallery_item(visual):
    image_url = ""
    if visual.uploaded_image:
        image_url = visual.uploaded_image.url
    elif visual.image_path:
        image_url = staticfiles_storage.url(visual.image_path)

    return {
        "id": visual.pk,
        "title": visual.title,
        "caption": visual.caption,
        "imagePath": visual.image_path,
        "imageUrl": image_url,
        "isActive": visual.is_active,
        "sortOrder": visual.sort_order,
    }
