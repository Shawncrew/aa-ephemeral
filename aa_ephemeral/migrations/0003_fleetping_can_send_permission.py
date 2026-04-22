from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aa_ephemeral', '0002_fleetping_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fleetping',
            options={
                'default_permissions': (),
                'permissions': [('can_send_fleet_ping', 'Can send hidden fleet pings')],
                'verbose_name': 'Fleet Ping',
                'verbose_name_plural': 'Fleet Pings',
            },
        ),
    ]
