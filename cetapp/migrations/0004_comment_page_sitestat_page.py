# Generated by Django 5.0.2 on 2025-07-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cetapp', '0003_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='page',
            field=models.CharField(default='trip', max_length=16),
        ),
        migrations.AddField(
            model_name='sitestat',
            name='page',
            field=models.CharField(default='trip', max_length=16),
        ),
    ]
