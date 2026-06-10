from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import ContactInquiry, HomePageContent, Solution


SOLUTION_MAP_SLOTS = {
    "vulture-uavs": {
        "url_name": "vulture_uavs",
        "link_class": "solution-link-vulture",
        "label_class": "solution-svg-label-vulture",
        "polygon_points": "505,146 711,302 438,404",
        "label_x": 552,
        "label_y": 266,
    },
    "skyguard": {
        "url_name": "skyguard",
        "link_class": "solution-link-skyguard",
        "label_class": "solution-svg-label-skyguard",
        "polygon_points": "438,404 711,302 660,604",
        "label_x": 603,
        "label_y": 437,
    },
    "tactical-data-link": {
        "url_name": "tactical_data_link",
        "link_class": "solution-link-tdl",
        "label_class": "solution-svg-label-tdl",
        "polygon_points": "438,404 660,604 415,674",
        "label_x": 504,
        "label_y": 524,
    },
    "vancom": {
        "url_name": "vancom",
        "link_class": "solution-link-vancom",
        "label_class": "solution-svg-label-vancom",
        "polygon_points": "711,302 893,499 660,604",
        "label_x": 755,
        "label_y": 431,
    },
}


def split_solution_label(title):
    words = title.split()
    if len(words) <= 1:
        return [title]

    lines = []
    current_line = []
    for word in words:
        candidate = " ".join([*current_line, word])
        if current_line and len(candidate) > 10:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    if current_line:
        lines.append(" ".join(current_line))

    return lines[:3]


def build_solution_map_items(solutions_queryset):
    solutions_by_slug = {
        solution.slug: solution
        for solution in solutions_queryset
    }
    map_items = []

    for slug, slot in SOLUTION_MAP_SLOTS.items():
        solution = solutions_by_slug.get(slug)
        if not solution:
            continue

        map_items.append({
            **slot,
            "title": solution.title,
            "label_lines": slot.get("label_lines") or split_solution_label(solution.title),
        })

    return map_items


def home(request):
    home_content = HomePageContent.objects.filter(
        key="main",
        is_active=True,
    ).first()

    return render(request, "website/home.html", {
        "current_page": "home",
        "home_content": home_content,
    })


def solutions(request):
    active_solutions = list(Solution.objects.filter(is_active=True))
    return render(request, "website/solutions.html", {
        "current_page": "solutions",
        "solutions": active_solutions,
        "solution_map_items": build_solution_map_items(active_solutions),
    })


def serialize_solution(solution):
    def visual_image_url(visual):
        if visual.uploaded_image:
            return visual.uploaded_image.url
        if visual.image_path:
            return staticfiles_storage.url(visual.image_path)
        return ""

    visuals = [
        {
            "title": visual.title,
            "caption": visual.caption,
            "image": visual_image_url(visual),
        }
        for visual in solution.visuals.filter(is_active=True)
    ]

    primary_image = ""
    if solution.primary_image:
        primary_image = solution.primary_image.url
    elif solution.primary_image_path:
        primary_image = staticfiles_storage.url(solution.primary_image_path)

    # مش هنضيف الصورة الأساسية للجاليري لو مستخدم مفعل تصفح الجاليري
    if primary_image and not solution.show_visual_nav:
        visuals.insert(0, {
            "title": solution.title,
            "caption": solution.visual_caption or solution.title,
            "image": primary_image,
        })

    logo_image = ""
    if solution.logo_image:
        logo_image = solution.logo_image.url
    elif solution.logo_image_path:
        logo_image = staticfiles_storage.url(solution.logo_image_path)

    return {
        "title": solution.title,
        "slug": solution.slug,
        "subtitle": solution.subtitle,
        "description": solution.description,
        "cta_text": solution.cta_text,
        "id": solution.solution_id,
        "illustration_type": solution.illustration_type,
        "image": primary_image,
        "logo": logo_image,
        "visual_caption": solution.visual_caption,
        "show_visual_nav": solution.show_visual_nav,
        "visuals": visuals,
    }


def solution_detail(request, slug):
    solution = (
        Solution.objects
        .filter(slug=slug, is_active=True)
        .prefetch_related("visuals")
        .first()
    )
    if not solution:
        return redirect("solutions")

    return render(request, "website/solution_detail.html", {
        "solution": serialize_solution(solution),
        "current_page": "solutions"
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            requested_solution_slug = cleaned.get("requested_solution_slug", "")
            requested_solution = None
            if requested_solution_slug:
                requested_solution = Solution.objects.filter(
                    slug=requested_solution_slug
                ).first()

            ContactInquiry.objects.create(
                organization=cleaned["organization"],
                name=cleaned["name"],
                email=cleaned["email"],
                phone=cleaned["phone"],
                message=cleaned["message"],
                inquiry_type=cleaned["inquiry_type"],
                requested_solution=requested_solution,
                requested_solution_slug=requested_solution_slug,
                source_path=request.path,
            )
            messages.success(request, "Your message has been successfully transmitted to our operations unit. We will contact you shortly.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "website/contact.html", {
        "form": form,
        "current_page": "contact"
    })
