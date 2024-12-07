# Generated by Django 5.1.3 on 2024-11-22 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoption',
            name='status',
            field=models.TextField(choices=[('APPROVED', 'approved'), ('REJECTED', 'rejected'), ('PENDING', 'pending')], default='PENDING'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.TextField(choices=[('SCHEDULED', 'scheduled'), ('CANCELLED', 'cancelled'), ('PENDING', 'pending')], default='PENDING'),
        ),
    ]
