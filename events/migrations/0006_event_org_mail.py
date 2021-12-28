# Generated by Django 3.2.10 on 2021-12-27 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_tickettype_show_tickets_remaining'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='org_mail',
            field=models.CharField(default='kontakt@example.com', help_text='Used as the Reply To address for e-mail notifications.', max_length=256, verbose_name='org mail'),
            preserve_default=False,
        ),
    ]