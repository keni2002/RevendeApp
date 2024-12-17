# Generated by Django 5.1.4 on 2024-12-17 14:32

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resell', '0003_remove_product_slug'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Categories'),
        ),
    ]
