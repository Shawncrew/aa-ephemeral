from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FleetPing",
            fields=[
                ("message_id", models.BigIntegerField(
                    primary_key=True,
                    serialize=False,
                    help_text="Discord message ID of the ping embed",
                )),
                ("secret", models.TextField(help_text="Secret fleet details revealed on button click")),
                ("posted_by", models.BigIntegerField(help_text="Discord user ID of the FC who posted the ping")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Ephemeral Ping",
                "verbose_name_plural": "Ephemeral Pings",
                "default_permissions": (),
            },
        ),
    ]
