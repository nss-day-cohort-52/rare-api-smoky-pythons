# Generated by Django 4.0.2 on 2022-02-17 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0005_alter_post_content_alter_post_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='demotionqueue',
            old_name='admin_id',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='demotionqueue',
            old_name='approver_one_id',
            new_name='approver_one',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='follower_id',
            new_name='follower',
        ),
    ]
