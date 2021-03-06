# Generated by Django 3.2.5 on 2021-07-22 04:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cellphone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=45)),
                ('postal_code', models.CharField(max_length=45)),
                ('country', models.CharField(max_length=45)),
                ('max_bid', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
