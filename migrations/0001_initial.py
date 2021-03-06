# Generated by Django 2.2.4 on 2020-01-30 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mine_id', models.IntegerField(blank=True, null=True)),
                ('shift_id', models.IntegerField(blank=True, null=True)),
                ('emp_id', models.IntegerField(blank=True, null=True)),
                ('ab_pr_date', models.DateField(blank=True, max_length=255, null=True)),
                ('ab_pr', models.CharField(blank=True, max_length=255, null=True)),
                ('leave_type', models.CharField(blank=True, max_length=255, null=True)),
                ('leave_no', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'attendance_emp',
            },
        ),
    ]
