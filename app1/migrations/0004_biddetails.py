# Generated by Django 4.1.2 on 2023-02-23 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_contactus_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Biddetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_bid', models.DateField(auto_created=True, auto_now=True)),
                ('SellerId', models.CharField(max_length=100)),
                ('buyerId', models.CharField(max_length=100)),
                ('bidamount', models.IntegerField(default='')),
                ('Description', models.TextField(default=None)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]