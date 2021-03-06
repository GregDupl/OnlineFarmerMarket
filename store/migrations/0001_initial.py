# Generated by Django 3.1 on 2020-08-24 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('rue', models.CharField(max_length=250)),
                ('complement', models.CharField(blank=True, max_length=250, null=True)),
                ('code_postal', models.CharField(max_length=5)),
                ('ville', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('phone', models.CharField(blank=True, max_length=256, null=True)),
                ('fk_adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.adress')),
            ],
        ),
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_client', models.CharField(max_length=50)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollectLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('fk_adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.adress')),
            ],
        ),
        migrations.CreateModel(
            name='CommandStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CommandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DirectWithdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fk_collect_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.collectlocation')),
            ],
        ),
        migrations.CreateModel(
            name='Historic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('fk_command_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.commandstatus')),
            ],
        ),
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('disponibility', models.BooleanField(default=True)),
                ('secret_code', models.IntegerField()),
                ('fk_admin_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.admincode')),
                ('fk_collect_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.collectlocation')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('fk_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.client')),
                ('fk_delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.delivery')),
                ('fk_direct_withdrawal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.directwithdrawal')),
                ('fk_locker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.locker')),
                ('historic_status', models.ManyToManyField(through='store.Historic', to='store.CommandStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('fk_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Unity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('stock', models.IntegerField()),
                ('image', models.URLField(default='no_url_product')),
                ('available', models.BooleanField(default=True)),
                ('fk_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('fk_unity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.unity')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('max_command', models.IntegerField()),
                ('fk_command_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.commandtype')),
                ('fk_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.day')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('fk_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('fk_variety', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variety')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='variety',
            field=models.ManyToManyField(through='store.OrderDetail', to='store.Variety'),
        ),
        migrations.AddField(
            model_name='historic',
            name='fk_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
        migrations.AddField(
            model_name='directwithdrawal',
            name='fk_time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.timeslot'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='fk_time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.timeslot'),
        ),
        migrations.AddField(
            model_name='collectlocation',
            name='fk_command_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.commandtype'),
        ),
        migrations.AddField(
            model_name='collectlocation',
            name='schedule',
            field=models.ManyToManyField(through='store.DirectWithdrawal', to='store.TimeSlot'),
        ),
        migrations.AddField(
            model_name='client',
            name='fk_client_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.clienttype'),
        ),
        migrations.AddField(
            model_name='client',
            name='variety',
            field=models.ManyToManyField(through='store.Cart', to='store.Variety'),
        ),
        migrations.AddField(
            model_name='cart',
            name='fk_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.client'),
        ),
        migrations.AddField(
            model_name='cart',
            name='fk_variety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variety'),
        ),
        migrations.AddConstraint(
            model_name='orderdetail',
            constraint=models.UniqueConstraint(fields=('fk_order', 'fk_variety'), name='unique_product_order'),
        ),
        migrations.AddConstraint(
            model_name='historic',
            constraint=models.UniqueConstraint(fields=('fk_order', 'fk_command_status'), name='unique_order_status'),
        ),
        migrations.AddConstraint(
            model_name='directwithdrawal',
            constraint=models.UniqueConstraint(fields=('fk_collect_location', 'fk_time_slot'), name='unique_direct_withdrawal'),
        ),
        migrations.AddConstraint(
            model_name='collectlocation',
            constraint=models.UniqueConstraint(fields=('fk_adress', 'fk_command_type'), name='unicque_collect_location'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('fk_client', 'fk_variety'), name='unique_product_cart'),
        ),
    ]
