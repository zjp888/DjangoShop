# Generated by Django 2.1.8 on 2019-07-22 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_image', models.ImageField(upload_to='freshApp/img', verbose_name='商品图片')),
                ('goods_number', models.IntegerField(verbose_name='商品数量库存')),
                ('goods_description', models.TextField(verbose_name='商品描述')),
                ('goods_date', models.DateField(verbose_name='出厂日期')),
                ('goods_safeDate', models.IntegerField(verbose_name='保质期')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_address', models.ImageField(upload_to='freshApp/img', verbose_name='图片地址')),
                ('img_description', models.TextField(max_length=32, verbose_name='图片描述')),
                ('goods_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FreshApp.Goods', verbose_name='商品id')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('nickname', models.CharField(blank=True, max_length=32, null=True, verbose_name='昵称')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='电话')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='freshApp/img', verbose_name='用户头像')),
                ('address', models.CharField(blank=True, max_length=32, null=True, verbose_name='地址')),
                ('card_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=32, verbose_name='店铺名称')),
                ('store_address', models.CharField(max_length=32, verbose_name='店铺地址')),
                ('store_descripton', models.TextField(verbose_name='店铺描述')),
                ('store_logo', models.ImageField(upload_to='freshApp/img', verbose_name='店铺logo')),
                ('store_phone', models.CharField(max_length=32, verbose_name='店铺电话')),
                ('store_money', models.FloatField(verbose_name='店铺注册资金')),
                ('user_id', models.IntegerField(verbose_name='店铺主人')),
            ],
        ),
        migrations.CreateModel(
            name='StoreType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_type', models.CharField(max_length=32, verbose_name='类型名称')),
                ('type_descripton', models.TextField(verbose_name='类型名称')),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='type',
            field=models.ManyToManyField(to='FreshApp.StoreType', verbose_name='店铺类型'),
        ),
        migrations.AddField(
            model_name='goods',
            name='store_id',
            field=models.ManyToManyField(to='FreshApp.Store', verbose_name='商品店铺'),
        ),
    ]
