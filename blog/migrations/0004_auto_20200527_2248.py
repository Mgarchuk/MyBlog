# Generated by Django 3.0.6 on 2020-05-27 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post_Image'),
        ),
    ]