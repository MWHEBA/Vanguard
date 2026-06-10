from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_solutionvisual_uploaded_image"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="solutionvisual",
            unique_together=set(),
        ),
    ]
