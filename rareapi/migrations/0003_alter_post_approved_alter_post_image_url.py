# Generated by Django 4.0.2 on 2022-02-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0002_post_tags_alter_rareuser_profile_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]