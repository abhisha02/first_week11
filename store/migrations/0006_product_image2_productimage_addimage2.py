# Generated by Django 4.2.9 on 2024-02-02 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_variation_image_variation_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='photos/products'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='addimage2',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='photos/products'),
        ),
    ]