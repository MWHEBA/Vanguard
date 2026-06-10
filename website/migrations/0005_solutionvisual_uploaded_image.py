from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_sitesettings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solutionvisual",
            name="image_path",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="solutionvisual",
            name="uploaded_image",
            field=models.FileField(blank=True, upload_to="solution-gallery/"),
        ),
    ]
