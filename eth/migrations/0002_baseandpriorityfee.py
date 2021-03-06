# Generated by Django 3.2.12 on 2022-02-16 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAndPriorityFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_fee', models.FloatField(blank=True, default=0.0, null=True)),
                ('max_priority_fee', models.FloatField(blank=True, default=0.0, null=True)),
                ('block_number', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
