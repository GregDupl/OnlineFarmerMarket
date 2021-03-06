# Generated by Django 3.1 on 2020-09-16 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200914_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistoric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('date_end', models.DateField(null=True)),
                ('date_cancellation', models.DateField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='historic',
            name='fk_command_status',
        ),
        migrations.RemoveField(
            model_name='historic',
            name='fk_order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='historic_status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='number',
        ),
        migrations.DeleteModel(
            name='CommandStatus',
        ),
        migrations.DeleteModel(
            name='Historic',
        ),
        migrations.AddField(
            model_name='orderhistoric',
            name='fk_order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
