# Generated by Django 4.1.6 on 2023-04-06 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_stores_image_bytes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packs',
            name='image_bytes',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]