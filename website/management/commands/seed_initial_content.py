from django.core.management.base import BaseCommand

from website.models import HomePageContent, SiteSettings, Solution, SolutionVisual


HOME_PAGE_CONTENT = {
    "key": "main",
    "browser_title": "Trusted Defense Solutions",
    "hero_title": "TRUSTED SOLUTIONS\nENGINEERED FOR MISSION SUCCESS.",
    "hero_description": (
        "Vanguard Technologies is an advanced defense technology company "
        "delivering integrated, smart, reliable, scalable mission-critical "
        "security special solutions."
    ),
    "cta_text": "OUR SOLUTIONS",
    "is_active": True,
}


SITE_SETTINGS = {
    "key": "main",
    "site_name": "Vanguard Technologies",
    "company_name": "Vanguard Technologies",
    "contact_email": "info@vanguard.example",
    "contact_phone": "",
    "linkedin_url": "",
    "footer_text": "ALL RIGHTS RESERVED 2026 © VANGUARD TECHNOLOGIES",
    "is_active": True,
}


SOLUTIONS = [
    {
        "slug": "vancom",
        "title": "VANCOM",
        "subtitle": "SECURE MILITARY COMMUNICATIONS",
        "description": (
            "VANCOM is a family of ruggedized control systems designed for military "
            "and mission-critical operations in harsh environments.\n"
            "Featuring hardened hardware and secure communication interfaces, it "
            "ensures reliable command and control under demanding conditions.\n"
            "The systems are rated IP65/IP67, providing protection against dust, "
            "water, and field exposure."
        ),
        "cta_text": "GET SPECS",
        "solution_id": "vancom",
        "illustration_type": "vancom_svg",
        "primary_image_path": "website/images/vancom-terminal.png",
        "visual_caption": "",
        "show_visual_nav": False,
        "sort_order": 10,
        "visuals": [],
    },
    {
        "slug": "vulture-uavs",
        "title": "VULTURE UAVs",
        "subtitle": "PRECISION SURVEILLANCE DRONES",
        "description": (
            "VULTURE UAVs are a mission-focused family of unmanned aerial systems "
            "delivering reliable intelligence, precision targeting support, and "
            "real-time operational awareness. Built on a modular architecture, "
            "they integrate advanced EO/IR payloads, secure long-range "
            "communications, and high-endurance airframes to provide continuous "
            "aerial coverage and geo-referenced data for rapid decision-making.\n"
            "VULTURE UAVs act as a force multiplier, enhancing targeting accuracy, "
            "validating mission data, and supporting post-strike assessment "
            "without interfering with fire-control systems."
        ),
        "cta_text": "GET SPECS",
        "solution_id": "vulture_uavs",
        "illustration_type": "vulture_svg",
        "primary_image_path": "",
        "visual_caption": "VULTURE i Group",
        "show_visual_nav": True,
        "sort_order": 20,
        "visuals": [
            ("VULTURE i Group", "VULTURE i Group", "website/images/vulture/h-07-2.png"),
            ("VULTURE X Group", "VULTURE X Group", "website/images/vulture/x-50-2.png"),
            ("VULTURE Jet X Group", "VULTURE Jet X Group", "website/images/vulture/jetx-1.png"),
            ("VULTURE S Group", "VULTURE S Group", "website/images/vulture/ser-2-1.png"),
        ],
    },
    {
        "slug": "skyguard",
        "title": "SkyGuard",
        "subtitle": "AIR DEFENSE RADAR SYSTEMS",
        "description": (
            "SKYGUARD is a modular, multi-layered counter-UAS (C-UAS) family of "
            "systems designed for the detection, tracking, and neutralization of "
            "aerial threats in contested environments.\n"
            "It integrates multi-band RF sensing, 3D radar, and EO/IR tracking "
            "within a unified command-and-control architecture.\n"
            "Real-time data fusion enables precise target classification, "
            "geo-location, and multi-threat tracking.\n"
            "SKYGUARD systems operate effectively under GNSS-denied and electronic "
            "warfare conditions, delivering scalable electronic countermeasures, "
            "including RF jamming and protocol-level disruption, to ensure "
            "persistent airspace control."
        ),
        "cta_text": "GET SPECS",
        "solution_id": "skyguard",
        "illustration_type": "skyguard_svg",
        "primary_image_path": "",
        "visual_caption": "VD 20",
        "show_visual_nav": True,
        "sort_order": 30,
        "visuals": [
            ("VD 20", "VD 20", "website/images/skyguard/vd-20.png"),
            ("VJ 11", "VJ 11", "website/images/skyguard/vj-11.png"),
            ("VS 30", "VS 30", "website/images/skyguard/vs-30.png"),
            ("V-MD 50", "V-MD 50", "website/images/skyguard/v-md-50.png"),
            ("Valcon F5", "Valcon F5", "website/images/skyguard/valcon-f5.png"),
            ("VR 10", "VR 10", "website/images/skyguard/vr-10.png"),
            ("V-OJ 20", "V-OJ 20", "website/images/skyguard/v-oj-20.png"),
            ("V-OD 40", "V-OD 40", "website/images/skyguard/v-od-40.png"),
        ],
    },
    {
        "slug": "tactical-data-link",
        "title": "Tactical Data Link",
        "subtitle": "ENCRYPTED TACTICAL NETWORK",
        "description": (
            "Advanced communication systems designed to enable secure, real-time "
            "exchange of mission-critical data between platforms, units, and "
            "command centers. These solutions support high-reliability "
            "transmission of video, telemetry, and targeting data across extended "
            "ranges, even in contested or degraded environments.\n"
            "Engineered for low latency, encryption, and interoperability, "
            "tactical data links enhance situational awareness, coordination, and "
            "decision-making across modern operations."
        ),
        "cta_text": "GET SPECS",
        "solution_id": "tactical_data_link",
        "illustration_type": "tactical_svg",
        "primary_image_path": "website/images/tactical-data-link/tactical-data-link-01.png",
        "visual_caption": "",
        "show_visual_nav": False,
        "sort_order": 40,
        "visuals": [],
    },
]


class Command(BaseCommand):
    help = "Seed initial editable website solutions and visuals."

    def handle(self, *args, **options):
        solution_count = 0
        visual_count = 0

        HomePageContent.objects.get_or_create(
            key=HOME_PAGE_CONTENT["key"],
            defaults=HOME_PAGE_CONTENT,
        )
        SiteSettings.objects.get_or_create(
            key=SITE_SETTINGS["key"],
            defaults=SITE_SETTINGS,
        )

        for item in SOLUTIONS:
            visuals = item["visuals"]
            solution_defaults = {
                key: value
                for key, value in item.items()
                if key != "visuals"
            }
            solution, created = Solution.objects.get_or_create(
                slug=item["slug"],
                defaults={**solution_defaults, "is_active": True},
            )
            solution_count += 1

            if created:
                active_image_paths = []
                for index, (title, caption, image_path) in enumerate(visuals, start=1):
                    SolutionVisual.objects.get_or_create(
                        solution=solution,
                        image_path=image_path,
                        defaults={
                            "title": title,
                            "caption": caption,
                            "sort_order": index * 10,
                            "is_active": True,
                        },
                    )
                    active_image_paths.append(image_path)
                    visual_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded home page content, {solution_count} solutions, and {visual_count} visuals."
            )
        )
