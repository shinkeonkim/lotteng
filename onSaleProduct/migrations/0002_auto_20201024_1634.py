# Generated by Django 3.1.1 on 2020-10-24 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onSaleProduct', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onsaleproduct',
            name='kinds',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]