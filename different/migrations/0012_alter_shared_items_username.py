# Generated by Django 3.2.4 on 2022-04-16 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('different', '0011_shared_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shared_items',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='different.bucket_list'),
        ),
    ]
