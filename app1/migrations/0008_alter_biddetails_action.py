# Generated by Django 4.1.2 on 2023-03-12 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_rename_notallotment_biddetails_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biddetails',
            name='action',
            field=models.BooleanField(default=False),
        ),
    ]
