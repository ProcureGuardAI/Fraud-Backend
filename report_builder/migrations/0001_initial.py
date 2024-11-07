# Generated by Django 5.1.3 on 2024-11-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.AutoField(primary_key=True, serialize=False)),
                ('contract_name', models.CharField(max_length=255)),
                ('contract_date', models.DateField()),
            ],
        ),
    ]
