from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_contactmessage_specsrequest"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(default="main", max_length=40, unique=True)),
                ("site_name", models.CharField(default="Vanguard Technologies", max_length=120)),
                ("company_name", models.CharField(default="Vanguard Technologies", max_length=120)),
                ("contact_email", models.EmailField(default="info@vanguard.example", max_length=254)),
                ("contact_phone", models.CharField(blank=True, max_length=40)),
                ("linkedin_url", models.URLField(blank=True)),
                ("footer_text", models.CharField(default="ALL RIGHTS RESERVED 2026 (C) VANGUARD TECHNOLOGIES", max_length=160)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "site settings",
                "verbose_name_plural": "site settings",
            },
        ),
    ]
