# Generated by Django 3.2.11 on 2022-01-22 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('country_code', models.IntegerField(blank=True, default=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('user_type', models.CharField(default='USER', max_length=20)),
                ('profile_pic', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(default=False, null=True)),
                ('facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_id', models.CharField(blank=True, max_length=255, null=True)),
                ('apple_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=1)),
                ('is_delete', models.BooleanField(default=0)),
                ('verification_key', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_connect_username', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_connect_username', models.CharField(blank=True, max_length=255, null=True)),
                ('openness', models.FloatField(blank=True, null=True)),
                ('extraversion', models.FloatField(blank=True, null=True)),
                ('emotional_stability', models.FloatField(blank=True, null=True)),
                ('agreeableness', models.FloatField(blank=True, null=True)),
                ('conscientiousness', models.FloatField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('is_notification', models.BooleanField(default=1)),
                ('usage_alert_time', models.IntegerField(blank=True, default=0, null=True)),
                ('email_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False)),
                ('refresh_token', models.CharField(default=False, max_length=500, null=True)),
                ('device_type', models.CharField(max_length=20)),
                ('device_token', models.CharField(default=False, max_length=255, null=True)),
                ('aws_arn', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='device_user', to='user.user')),
            ],
            options={
                'db_table': 'device',
            },
        ),
    ]
