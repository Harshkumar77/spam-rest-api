# Generated by Django 5.0.3 on 2024-03-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_management', '0003_alter_spamreport_spam_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spamreport',
            old_name='spam_by',
            new_name='reported_by',
        ),
        migrations.RemoveField(
            model_name='spamreport',
            name='spam_reason',
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
