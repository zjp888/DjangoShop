# Generated by Django 2.1.8 on 2019-07-29 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0002_orderdetail_goods_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Buyer.Address', verbose_name='订单地址'),
        ),
    ]
