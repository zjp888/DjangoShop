# Generated by Django 2.1.8 on 2019-07-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='goods_image',
            field=models.ImageField(default='/static/buyer/images', upload_to='', verbose_name='商品图片'),
            preserve_default=False,
        ),
    ]
