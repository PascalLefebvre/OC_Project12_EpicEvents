# Generated by Django 4.1.7 on 2023-03-31 06:40

import crm.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0002_alter_contractstatus_options_contract_payment_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='crm.client'), on_delete=models.SET(crm.models.get_sentinel_user), related_name='signed_contract', to=settings.AUTH_USER_MODEL),
        ),
    ]
