# Generated by Django 4.2.16 on 2024-09-12 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('traders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trader',
            options={'permissions': [('post_products', 'Can post products')]},
        ),
    ]
