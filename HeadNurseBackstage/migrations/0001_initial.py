# Generated by Django 2.2 on 2022-12-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeadNurseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=-1, max_length=45)),
                ('username', models.CharField(default=-1, max_length=45)),
                ('password', models.CharField(default=-1, max_length=45)),
                ('workPermitNumber', models.CharField(default=-1, max_length=45)),
                ('workPermitPassword', models.CharField(default=-1, max_length=45)),
                ('login_jwt', models.CharField(default=-1, max_length=500)),
            ],
        ),
    ]
