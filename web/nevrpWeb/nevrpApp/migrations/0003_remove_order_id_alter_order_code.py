# Generated by Django 4.2.2 on 2023-06-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nevrpApp', '0002_node_remove_order_description_remove_order_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=400, primary_key=True, serialize=False, unique=True),
        ),
    ]
