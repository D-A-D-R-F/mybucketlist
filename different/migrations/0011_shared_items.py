# Generated by Django 3.2.4 on 2022-04-16 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('different', '0010_auto_20220414_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shared_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=250)),
                ('comment', models.CharField(default='', max_length=500)),
                ('completed_item', models.CharField(default='', max_length=350)),
            ],
        ),
    ]
