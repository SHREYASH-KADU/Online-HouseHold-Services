# Generated by Django 4.1.7 on 2023-03-31 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_client_service_user_is_worker_transactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='category_image',
            new_name='image',
        ),
    ]
