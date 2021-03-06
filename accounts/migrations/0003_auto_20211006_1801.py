# Generated by Django 3.2.8 on 2021-10-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='lga',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, choices=[('ABIA', 'ABIA'), ('ABUJA', 'ABUJA'), ('ADAMAWA', 'ADAMAWA'), ('AKWA IBOM', 'AKWA IBOM'), ('ANAMBRA', 'ANAMBRA'), ('BAUCHI', 'BAUCHI'), ('BAYELSA', 'BAYELSA'), ('BENUE', 'BENUE'), ('BORNO', 'BORNO'), ('CROSS RIVER', 'CROSS RIVER'), ('DELTA', 'DELTA'), ('EBONYI', 'EBONYI'), ('EDO', 'EDO'), ('EKITI', 'EKITI'), ('ENUGU', 'ENUGU'), ('GOMBE', 'GOMBE'), ('IMO', 'IMO'), ('JIGAWA', 'JIGAWA'), ('KADUNA', 'KADUNA'), ('KANO', 'KANO'), ('KATSINA', 'KATSINA'), ('KEBBI', 'KEBBI'), ('KOGI', 'KOGI'), ('KWARA', 'KWARA'), ('LAGOS', 'LAGOS'), ('NASSARAWA', 'NASSARAWA'), ('NIGER', 'NIGER'), ('OGUN', 'OGUN'), ('ONDO', 'ONDO'), ('OSUN', 'OSUN'), ('OYO', 'OYO'), ('PLATEAU', 'PLATEAU'), ('RIVERS', 'RIVERS'), ('SOKOTO', 'SOKOTO'), ('TARABA', 'TARABA'), ('YOBE', 'YOBE'), ('ZAMFARA', 'ZAMFARA'), ('NON NIGERIAN', 'NON NIGERIAN')], max_length=50, null=True),
        ),
    ]
