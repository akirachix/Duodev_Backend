# Generated by Django 4.2.16 on 2024-09-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_sales', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_orders', models.IntegerField()),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
        migrations.AlterField(
            model_name='order',
            name='date_placed',
            field=models.DateField(auto_now_add=True),
        ),
    ]
