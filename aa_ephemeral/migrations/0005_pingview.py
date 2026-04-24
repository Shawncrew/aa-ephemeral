from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aa_ephemeral', '0004_fleetping_posted_by_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PingView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(help_text='Discord user ID of the viewer')),
                ('user_name', models.CharField(default='', help_text='Display name at time of viewing', max_length=100)),
                ('first_viewed_at', models.DateTimeField(auto_now_add=True)),
                ('ping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='aa_ephemeral.fleetping')),
            ],
            options={
                'verbose_name': 'Ping View',
                'verbose_name_plural': 'Ping Views',
                'default_permissions': (),
                'unique_together': {('ping', 'user_id')},
            },
        ),
    ]
