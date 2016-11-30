# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FpsData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currentPage', models.TextField()),
                ('fps', models.BigIntegerField()),
                ('jankCount', models.BigIntegerField()),
                ('packageName', models.TextField()),
                ('versionCode', models.TextField()),
            ],
        ),
    ]
