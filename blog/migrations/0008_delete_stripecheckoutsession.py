# Generated by Django 4.2.5 on 2023-09-21 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_stripecheckoutsession'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StripeCheckoutSession',
        ),
    ]
