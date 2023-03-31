# Generated by Django 4.1.7 on 2023-03-31 06:50

import crm.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0003_alter_contract_sales_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(on_delete=models.SET(crm.models.get_sentinel_user), related_name='signed_contract', to=settings.AUTH_USER_MODEL),
        ),
    ]