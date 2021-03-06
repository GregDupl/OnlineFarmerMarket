# Generated by Django 3.1 on 2020-09-08 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200908_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='fk_time_slot',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='max_command',
        ),
        migrations.AddField(
            model_name='directwithdrawal',
            name='max_command',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='fk_delivery',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.delivery'),
        ),
        migrations.AlterField(
            model_name='order',
            name='fk_locker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.locker'),
        ),
        migrations.CreateModel(
            name='DeliverySlots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_command', models.PositiveIntegerField()),
                ('delivery_area', models.CharField(max_length=250)),
                ('fk_time_slot', models.ForeignKey(limit_choices_to={'fk_command_type': 3}, on_delete=django.db.models.deletion.CASCADE, to='store.timeslot')),
            ],
        ),
        migrations.AddField(
            model_name='delivery',
            name='fk_delivery_slot',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.deliveryslots'),
        ),
    ]
