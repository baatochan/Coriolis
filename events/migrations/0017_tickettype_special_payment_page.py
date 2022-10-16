# Generated by Django 3.2.13 on 2022-04-20 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_eventpage_page_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='special_payment_page',
            field=models.ForeignKey(help_text='If you want to use special payment instructions for this ticket type, create an Event Page with those, set its type to Ticket Payment Instructions and select it here.', limit_choices_to={'page_type': 'ticket-payment-info'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventpage', verbose_name='special payment page'),
        ),
    ]