from django.core.management.base import BaseCommand

from allianceauth.services.modules.discord.models import DiscordUser

from aa_ephemeral.models import FleetPing
from aa_ephemeral.watermark import decode_invisible, generate_watermark


class Command(BaseCommand):
    help = "Identify which Discord user a leaked fleet ping belongs to."

    def add_arguments(self, parser):
        parser.add_argument("message_id", type=int, help="Discord message ID of the fleet ping")
        parser.add_argument(
            "text",
            type=str,
            nargs="?",
            default=None,
            help="Paste the full leaked message text to decode the invisible watermark (optional)",
        )
        parser.add_argument(
            "--code",
            type=str,
            default=None,
            help="Visible msgid code to look up instead (e.g. A3F2B1C4)",
        )

    def handle(self, *args, **options):
        message_id = options["message_id"]
        pasted_text = options.get("text")
        visible_code = options.get("code")

        try:
            ping = FleetPing.objects.get(message_id=message_id)
        except FleetPing.DoesNotExist:
            self.stderr.write(f"No fleet ping found with message ID {message_id}.")
            return

        self.stdout.write(f"Checking ping sent by {ping.posted_by_name}...")

        # Try invisible watermark first if text was pasted
        code = None
        if pasted_text:
            code = decode_invisible(pasted_text)
            if code:
                self.stdout.write(f"Invisible watermark decoded: {code}")
            else:
                self.stdout.write(self.style.WARNING("No invisible watermark found in pasted text."))

        # Fall back to visible code
        if not code and visible_code:
            code = visible_code.upper()

        if not code:
            self.stderr.write("Provide either pasted text or --code to identify the leak.")
            return

        for discord_user in DiscordUser.objects.all():
            if generate_watermark(discord_user.uid, message_id) == code:
                user = discord_user.user
                self.stdout.write(
                    self.style.ERROR(
                        f"MATCH FOUND: Discord UID {discord_user.uid} — "
                        f"Auth user: {user.username} ({user.email})"
                    )
                )
                return

        self.stdout.write(self.style.WARNING("No match found for that code."))
