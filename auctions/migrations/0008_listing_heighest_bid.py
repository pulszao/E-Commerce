# Generated by Django 3.0.8 on 2020-10-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20201005_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='heighest_bid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
