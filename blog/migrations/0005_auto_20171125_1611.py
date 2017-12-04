# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-25 16:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171109_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(verbose_name='建立时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=20, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(verbose_name='最后修改时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=60, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='阅读量'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, verbose_name='标签'),
        ),
    ]
