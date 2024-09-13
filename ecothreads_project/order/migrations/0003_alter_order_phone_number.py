from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
