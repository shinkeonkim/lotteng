# Generated by Django 3.1.1 on 2020-10-22 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_authnumber'),
        ('customerPurchase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpurchase',
            name='auth_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.authnumber'),
        ),
    ]
