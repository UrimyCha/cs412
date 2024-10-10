# Generated by Django 5.1.1 on 2024-10-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.TextField()),
                ('city', models.TextField()),
                ('email', models.TextField()),
                ('lastname', models.TextField()),
                ('image_url', models.URLField()),
            ],
        ),
    ]