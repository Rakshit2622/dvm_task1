# Generated by Django 4.2.1 on 2023-05-19 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(max_length=100)),
                ('item_price', models.FloatField()),
                ('item_description', models.CharField(max_length=400)),
                ('item_image', models.ImageField(upload_to='vendor_items_pics')),
                ('item_stock', models.PositiveIntegerField()),
                ('item_orders', models.PositiveIntegerField(default=0)),
                ('is_listed', models.BooleanField(default=True)),
                ('item_vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_item', to='users.vendoruser')),
            ],
        ),
    ]
