# Generated by Django 4.2.2 on 2023-06-18 10:54

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('price', models.FloatField(default=0.0, max_length=10)),
                ('image', models.ImageField(blank=True, default='orders/order_default.png', null=True, upload_to='orders/')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=400, null=True, unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]