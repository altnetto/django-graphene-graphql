# Generated by Django 4.0.4 on 2022-05-01 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='graphql_api.user')),
            ],
        ),
    ]