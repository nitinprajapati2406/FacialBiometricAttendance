# Generated by Django 4.2.4 on 2023-09-20 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AttendanceApp', '0006_remove_faceid_faceid_faceid_face_encodings_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faceid',
            old_name='face_encodings_json',
            new_name='faceid',
        ),
    ]