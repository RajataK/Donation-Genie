from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foodbanks", "0004_foodbanksettings_qrscan_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="generatedrecipe",
            name="dietary_tags",
            field=models.JSONField(default=list),
        ),
    ]
