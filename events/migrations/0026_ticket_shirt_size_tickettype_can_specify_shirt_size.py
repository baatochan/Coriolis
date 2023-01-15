# Generated by Django 4.1.5 on 2023-01-15 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0025_tickettype_purchase_rate_limit_secs"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="shirt_size",
            field=models.CharField(
                blank=True,
                help_text="Shirt size chosen by the attendee.",
                max_length=4,
                verbose_name="shirt size",
            ),
        ),
        migrations.AddField(
            model_name="tickettype",
            name="can_specify_shirt_size",
            field=models.BooleanField(
                default=False,
                help_text="Determines if a shirt size can be personalized.",
                verbose_name="can specify shirt size",
            ),
        ),
    ]
