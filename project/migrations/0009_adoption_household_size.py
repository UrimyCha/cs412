# Generated by Django 5.1.3 on 2024-12-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_adoption_address_adoption_children_num_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adoption',
            name='household_size',
            field=models.IntegerField(default=1, null=True),
        ),
    ]