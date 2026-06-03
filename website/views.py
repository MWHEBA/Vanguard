from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# الصفحة الرئيسية للموقع
def home(request):
    return render(request, "website/home.html", {
        "current_page": "home"
    })

# صفحة الحلول التكنولوجية الرئيسية (بتعرض الـ 3D Model أو الـ SVG Fallback)
def solutions(request):
    return render(request, "website/solutions.html", {
        "current_page": "solutions"
    })

# تفاصيل كل منتج أو حل تكنولوجي بناءً على الـ slug
def solution_detail(request, slug):
    solutions_data = {
        "vancom": {
            "title": "VANCOM",
            "subtitle": "SECURE MILITARY COMMUNICATIONS",
            "description": "VANCOM™ is a family of ruggedized control systems designed for military and mission-critical operations in harsh environments.\nFeaturing hardened hardware and secure communication interfaces, it ensures reliable command and control under demanding conditions.\nThe systems are rated IP65/IP67, providing protection against dust, water, and field exposure.",
            "cta_text": "GET SPECS",
            "id": "vancom",
            "illustration_type": "vancom_svg",
            "image": "website/images/vancom-terminal.png"
        },
        "vulture-uavs": {
            "title": "VULTURE UAVs",
            "subtitle": "PRECISION SURVEILLANCE DRONES",
            "description": "VULTURE UAVs are a mission-focused family of unmanned aerial systems delivering reliable intelligence, precision targeting support, and real-time operational awareness. Built on a modular architecture, they integrate advanced EO/IR payloads, secure long-range communications, and high-endurance airframes to provide continuous aerial coverage and geo-referenced data for rapid decision-making.\nVULTURE UAVs act as a force multiplier—enhancing targeting accuracy, validating mission\ndata, and supporting post-strike assessment without interfering with fire-control systems.",
            "cta_text": "GET SPECS",
            "id": "vulture_uavs",
            "illustration_type": "vulture_svg",
            "image": "",
            "visual_caption": "VULTURE i Group",
            "show_visual_nav": True,
            "visuals": [
                {
                    "title": "VULTURE i Group",
                    "caption": "VULTURE i Group",
                    "image": "website/images/vulture/h-07-2.png"
                },
                {
                    "title": "VULTURE X Group",
                    "caption": "VULTURE X Group",
                    "image": "website/images/vulture/x-50-2.png"
                },
                {
                    "title": "VULTURE Jet X Group",
                    "caption": "VULTURE Jet X Group",
                    "image": "website/images/vulture/jetx-1.png"
                },
                {
                    "title": "VULTURE S Group",
                    "caption": "VULTURE S Group",
                    "image": "website/images/vulture/ser-2-1.png"
                }
            ]
        },
        "skyguard": {
            "title": "SkyGuard",
            "subtitle": "AIR DEFENSE RADAR SYSTEMS",
            "description": "SKYGUARD™ is a modular, multi-layered counter-UAS (C-UAS) family of systems designed for the detection, tracking, and neutralization of aerial threats in contested environments.\nit integrates multi-band RF sensing, 3D radar, and EO/IR tracking within a unified command-and-control architecture.\nreal-time data fusion enables precise target classification, geo-location, and multi-threat tracking.\nSKYGUARD™ systems operate effectively under GNSS-denied and electronic warfare conditions, delivering scalable electronic countermeasures—including RF jamming and protocol-level disruption—to ensure persistent airspace control.",
            "cta_text": "GET SPECS",
            "id": "skyguard",
            "illustration_type": "skyguard_svg",
            "image": "",
            "visual_caption": "VD 20",
            "show_visual_nav": True,
            "visuals": [
                {
                    "title": "VD 20",
                    "caption": "VD 20",
                    "image": "website/images/skyguard/vd-20.png"
                },
                {
                    "title": "VJ 11",
                    "caption": "VJ 11",
                    "image": "website/images/skyguard/vj-11.png"
                },
                {
                    "title": "VS 30",
                    "caption": "VS 30",
                    "image": "website/images/skyguard/vs-30.png"
                },
                {
                    "title": "V-MD 50",
                    "caption": "V-MD 50",
                    "image": "website/images/skyguard/v-md-50.png"
                },
                {
                    "title": "Valcon F5",
                    "caption": "Valcon F5",
                    "image": "website/images/skyguard/valcon-f5.png"
                },
                {
                    "title": "VR 10",
                    "caption": "VR 10",
                    "image": "website/images/skyguard/vr-10.png"
                },
                {
                    "title": "V-OJ 20",
                    "caption": "V-OJ 20",
                    "image": "website/images/skyguard/v-oj-20.png"
                },
                {
                    "title": "V-OD 40",
                    "caption": "V-OD 40",
                    "image": "website/images/skyguard/v-od-40.png"
                }
            ]
        },
        "tactical-data-link": {
            "title": "Tactical Data Link",
            "subtitle": "ENCRYPTED TACTICAL NETWORK",
            "description": "advanced communication systems designed to enable secure, real-time exchange of mission-critical data between platforms, units, and command centers. these solutions support high-reliability transmission of video, telemetry, and targeting data across extended ranges, even in contested or degraded environments.\nengineered for low latency, encryption, and interoperability, tactical data links enhance\nsituational awareness, coordination, and decision-making across modern operations.",
            "cta_text": "GET SPECS",
            "id": "tactical_data_link",
            "illustration_type": "tactical_svg",
            "image": "website/images/tactical-data-link/tactical-data-link-01.png"
        }
    }
    
    solution = solutions_data.get(slug)
    if not solution:
        return redirect("solutions")
        
    return render(request, "website/solution_detail.html", {
        "solution": solution,
        "current_page": "solutions"
    })

# صفحة التواصل مع معالجة الفورم وعرض رسالة النجاح
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # في المرحلة الأولى مفيش حفظ في قاعدة البيانات أو إرسال إيميل
            # فقط بنعرض رسالة نجاح للمستخدم
            messages.success(request, "SECURE TRANSMISSION RECEIVED. OUR OPERATIONS UNIT WILL CONTACT YOU.")
            return redirect("contact")
    else:
        form = ContactForm()
        
    return render(request, "website/contact.html", {
        "form": form,
        "current_page": "contact"
    })
