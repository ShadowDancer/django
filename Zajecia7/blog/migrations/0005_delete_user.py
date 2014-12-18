# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141211_2309'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
