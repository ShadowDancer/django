# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_account_operation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='target',
        ),
    ]
