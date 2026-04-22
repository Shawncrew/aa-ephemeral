from django.db import models


class FleetPing(models.Model):
    """Stores the secret contents of a hidden fleet ping, keyed by Discord message ID."""

    message_id = models.BigIntegerField(primary_key=True, help_text="Discord message ID of the ping embed")
    secret = models.TextField(help_text="Secret fleet details revealed on button click")
    posted_by = models.BigIntegerField(help_text="Discord user ID of the FC who posted the ping")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_permissions = ()
        verbose_name = "Fleet Ping"
        verbose_name_plural = "Fleet Pings"
        permissions = (
            ("can_send_fleet_ping", "Can send hidden fleet pings"),
        )

    def __str__(self):
        return f"FleetPing {self.message_id}"
