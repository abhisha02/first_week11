# Generated by Django 4.2.9 on 2024-01-23 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_alter_profile_uid_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000020FA2BABEC0>', max_length=200),
        ),
    ]
