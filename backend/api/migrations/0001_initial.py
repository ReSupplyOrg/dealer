# Generated by Django 4.1.6 on 2023-02-12 02:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('deletion', models.DateTimeField(auto_now=True)),
                ('phone', models.TextField()),
                ('confirmed', models.BooleanField()),
                ('image_bytes', models.BinaryField(null=True)),
                ('names', models.TextField()),
                ('username', models.TextField()),
                ('password_salt', models.TextField()),
                ('password_hash', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('deletion', models.DateTimeField(auto_now=True)),
                ('phone', models.TextField()),
                ('confirmed', models.BooleanField()),
                ('image_bytes', models.BinaryField(null=True)),
                ('name', models.TextField()),
                ('rating', models.FloatField()),
                ('address', models.TextField()),
                ('username', models.TextField()),
                ('password_salt', models.TextField()),
                ('password_hash', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('deletion', models.DateTimeField(auto_now=True)),
                ('rating', models.FloatField()),
                ('client_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clients')),
                ('store_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stores')),
            ],
        ),
        migrations.CreateModel(
            name='Packs',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('deletion', models.DateTimeField(auto_now=True)),
                ('image_bytes', models.BinaryField(null=True)),
                ('stock', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('name', models.TextField()),
                ('pack_type', models.TextField()),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stores')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modification', models.DateTimeField(auto_now=True)),
                ('deletion', models.DateTimeField(auto_now=True)),
                ('payed_price', models.IntegerField()),
                ('client_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clients')),
                ('pack_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.packs')),
                ('store_uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stores')),
            ],
        ),
    ]
