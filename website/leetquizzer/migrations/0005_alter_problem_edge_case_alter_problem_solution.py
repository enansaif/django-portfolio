# Generated by Django 4.2.2 on 2023-06-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leetquizzer', '0004_problem_option1_problem_option2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='edge_case',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='solution',
            field=models.TextField(null=True),
        ),
    ]
