# Generated by Django 3.2.5 on 2022-08-21 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computers',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False, unique=True)),
                ('bios_serial', models.TextField(blank=True, db_column='BIOS_Serial', null=True, unique=True)),
                ('comp_name', models.TextField(blank=True, db_column='Comp_Name', null=True)),
                ('last_timecreated', models.TextField(blank=True, db_column='Last_TimeCreated', null=True)),
                ('csvlog', models.BinaryField(db_column='Csv_Log')),
                ('system', models.TextField(blank=True, db_column='System', null=True)),
                ('release', models.TextField(blank=True, db_column='Release', null=True)),
                ('version', models.TextField(blank=True, db_column='Version', null=True)),
                ('machine', models.TextField(blank=True, db_column='Machine', null=True)),
            ],
            options={
                'db_table': 'Computers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False, unique=True)),
                ('logged_on', models.TextField(blank=True, db_column='Logged_On', null=True)),
            ],
            options={
                'db_table': 'Info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ipees',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False, unique=True)),
                ('ip', models.TextField(blank=True, db_column='IP', null=True, unique=True)),
                ('status', models.IntegerField(blank=True, db_column='Status', null=True)),
            ],
            options={
                'db_table': 'IPees',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False, unique=True)),
                ('logged_on_t', models.TextField(blank=True, db_column='Logged_On_track', null=True)),
            ],
            options={
                'db_table': 'Track',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False, unique=True)),
                ('user', models.TextField(blank=True, db_column='User', null=True)),
                ('domain', models.TextField(blank=True, db_column='Domain', null=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': False,
            },
        ),
    ]