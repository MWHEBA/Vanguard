from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_remove_solutionvisual_unique_image_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="solution",
            name="primary_image",
            field=models.FileField(blank=True, upload_to="solution-primary/"),
        ),
    ]
