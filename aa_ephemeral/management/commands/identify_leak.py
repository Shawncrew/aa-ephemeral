from django.core.management.base import BaseCommand

from allianceauth.services.modules.discord.models import DiscordUser

from aa_ephemeral.models import FleetPing
from aa_ephemeral.watermark import decode_invisible, generate_visible_code, generate_watermark


class Command(BaseCommand):
    help = "Identify which Discord user a leaked fleet ping belongs to."

    def add_arguments(self, parser):
        parser.add_argument("message_id", type=int, help="Discord message ID of the fleet ping")
        parser.add_argument(
            "text",
            type=str,
            nargs="?",
            default=None,
            help="Paste the full leaked message text to decode the invisible watermark",
        )
        parser.add_argument(
            "--code",
            type=str,
            default=None,
            help="The 6-digit code visible at the end of the timestamp (e.g. 125208)",
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

        # Try invisible watermark from pasted text first
        invisible_code = None
        if pasted_text:
            invisible_code = decode_invisible(pasted_text)
            if invisible_code:
                self.stdout.write(f"Invisible watermark decoded: {invisible_code}")
            else:
                self.stdout.write(self.style.WARNING("No invisible watermark found in pasted text."))

        all_discord_users = DiscordUser.objects.all()

        # Match on invisible watermark
        if invisible_code:
            for discord_user in all_discord_users:
                if generate_watermark(discord_user.uid, message_id) == invisible_code:
                    self._print_match(discord_user)
                    return

        # Match on visible 6-digit code
        if visible_code:
            for discord_user in all_discord_users:
                if generate_visible_code(discord_user.uid, message_id) == visible_code.zfill(6):
                    self._print_match(discord_user)
                    return

        self.stdout.write(self.style.WARNING("No match found."))

    def _print_match(self, discord_user):
        user = discord_user.user
        self.stdout.write(
            self.style.ERROR(
                f"MATCH FOUND: Discord UID {discord_user.uid} — "
                f"Auth user: {user.username} ({user.email})"
            )
        )
