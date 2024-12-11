# Generated by Django 5.1.3 on 2024-11-22 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_cat_name_alter_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoption',
            name='status',
            field=models.CharField(choices=[('APPROVED', 'approved'), ('REJECTED', 'rejected'), ('PENDING', 'pending')], default='PENDING', max_length=8),
        ),
    ]