"""Sync Meta options on FleetPing that had no migration. State-only."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aa_ephemeral", "0005_pingview"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fleetping",
            options={
                "default_permissions": (),
                "permissions": (("can_send_fleet_ping", "Can send hidden fleet pings"),),
                "verbose_name": "Fleet Ping",
                "verbose_name_plural": "Fleet Pings",
            },
        ),
    ]
