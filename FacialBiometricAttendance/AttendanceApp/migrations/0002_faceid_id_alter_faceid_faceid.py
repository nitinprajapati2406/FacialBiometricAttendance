# Generated by Django 4.2.4 on 2023-09-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AttendanceApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faceid',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faceid',
            name='faceid',
            field=models.TextField(),
        ),
    ]