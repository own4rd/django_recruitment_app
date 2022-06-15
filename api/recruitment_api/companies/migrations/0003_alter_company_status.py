# Generated by Django 3.2.6 on 2022-06-15 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_company_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('Layoffs', 'Layoffs'), ('Contratação parada', 'Hiring Freeze'), ('Contratando', 'Hiring')], default='Contratando', max_length=30, verbose_name='Status'),
        ),
    ]
