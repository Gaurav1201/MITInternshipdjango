# Generated by Django 5.1.4 on 2024-12-13 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_rename_tb_course1_tb_course_alter_tb_course_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='tb_course_faculty_mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=45)),
                ('faculty_id', models.CharField(max_length=45)),
                ('academic_year', models.IntegerField()),
            ],
            options={
                'db_table': 'tb_course_faculty_mapping',
            },
        ),
        migrations.RemoveField(
            model_name='tb_course',
            name='academic_year',
        ),
        migrations.RemoveField(
            model_name='tb_course',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='tb_course',
            name='course_number',
        ),
        migrations.RemoveField(
            model_name='tb_course',
            name='faculty_id',
        ),
        migrations.AddField(
            model_name='tb_course',
            name='course_code',
            field=models.CharField(default='DEFAULT_CODE', max_length=45, primary_key=True, serialize=False),
        ),
    ]