# Generated by Django 4.1.6 on 2023-02-13 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_clients_password_hash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='image_bytes',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clients',
            name='password_hash',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='clients',
            name='password_salt',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='stores',
            name='image_bytes',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='stores',
            name='password_hash',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='stores',
            name='password_salt',
            field=models.BinaryField(),
        ),
    ]