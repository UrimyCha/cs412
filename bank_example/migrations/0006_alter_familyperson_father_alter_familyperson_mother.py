# Generated by Django 5.1.3 on 2024-11-19 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_example', '0005_familyperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familyperson',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='father_person', to='bank_example.familyperson'),
        ),
        migrations.AlterField(
            model_name='familyperson',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother_person', to='bank_example.familyperson'),
        ),
    ]
