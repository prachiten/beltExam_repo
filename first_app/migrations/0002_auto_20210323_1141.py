# Generated by Django 2.2 on 2021-03-23 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirm_password',
        ),
        migrations.DeleteModel(
            name='Giraffe',
        ),
        migrations.AddField(
            model_name='organization',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_created', to='first_app.User'),
        ),
        migrations.AddField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(related_name='org_joined', to='first_app.User'),
        ),
    ]
