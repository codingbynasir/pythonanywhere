# Generated by Django 2.0.4 on 2018-05-07 14:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medical', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package_billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.IntegerField()),
                ('account_number', models.CharField(max_length=100)),
                ('transaction_id', models.CharField(max_length=100)),
                ('paid_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Not Paid', 'Not paid'), ('Partially Paid', 'Partially Paid'), ('Fully Paid', 'Fully Paid')], default='Not Paid', max_length=20)),
                ('token_num', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('verify', models.BooleanField(default=False)),
                ('test_taking_date', models.DateField(blank=True, null=True)),
                ('test_taking_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('On hold', 'On hold'), ('Completed', 'Completed'), ('Refunded', 'Refunded'), ('Archived', 'Archived')], default='Processing', max_length=100)),
                ('package_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Test_billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.IntegerField()),
                ('account_number', models.CharField(max_length=100)),
                ('transaction_id', models.CharField(max_length=100)),
                ('paid_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Not Paid', 'Not paid'), ('Partially Paid', 'Partially Paid'), ('Fully Paid', 'Fully Paid')], default='Not Paid', max_length=20)),
                ('token_num', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('verify', models.BooleanField(default=False)),
                ('is_completed', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=20)),
                ('test_taking_date', models.DateField(blank=True, default=datetime.date(2018, 5, 7), null=True)),
                ('test_taking_time', models.TimeField(blank=True, default=datetime.time(20, 35, 31, 538960), null=True)),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('On hold', 'On hold'), ('Completed', 'Completed'), ('Refunded', 'Refunded'), ('Archived', 'Archived')], default='Processing', max_length=100)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.has_test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
        migrations.AddField(
            model_name='test_billing',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order_billing.Test_order'),
        ),
        migrations.AddField(
            model_name='package_billing',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order_billing.Package_order'),
        ),
    ]
