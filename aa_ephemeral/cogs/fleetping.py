import logging

import discord
from discord.ext import commands

from aadiscordbot.cogs.utils.decorators import sender_has_perm

from aa_ephemeral.models import FleetPing
from aa_ephemeral.watermark import format_sent_by, inject_watermark

logger = logging.getLogger(__name__)

REVEAL_BUTTON_PREFIX = "fleetping_reveal:"


class RevealView(discord.ui.View):
    """
    Persistent button view attached to a fleet ping embed.
    The custom_id encodes the message_id so the secret can be fetched from the
    database after a bot restart without any in-memory state.
    """

    def __init__(self, message_id: int):
        super().__init__(timeout=None)
        self.message_id = message_id

        button = discord.ui.Button(
            label="Open",
            style=discord.ButtonStyle.danger,
            emoji="🔒",
            custom_id=f"{REVEAL_BUTTON_PREFIX}{message_id}",
        )
        button.callback = self.reveal
        self.add_item(button)

    async def reveal(self, interaction: discord.Interaction):
        try:
            ping = FleetPing.objects.get(message_id=self.message_id)
            watermarked_secret = inject_watermark(ping.secret, interaction.user.id, self.message_id)
            sent_by = format_sent_by(ping.posted_by_name, interaction.user.id, self.message_id, ping.created_at)
            content = f"{watermarked_secret}\n\n{sent_by}"
        except FleetPing.DoesNotExist:
            content = "Fleet ping details are no longer available."
        except Exception as e:
            logger.error(f"FleetPing lookup failed for message {self.message_id}: {e}")
            content = "Something went wrong retrieving the fleet details."

        await interaction.response.send_message(content, ephemeral=True)


class FleetPingCog(commands.Cog):
    """
    Post a hidden fleet ping in a channel with a reveal button.
    The secret message is stored in the database so buttons survive bot restarts.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Re-register all persistent RevealViews from the database on startup."""
        count = 0
        for ping in FleetPing.objects.all():
            self.bot.add_view(RevealView(message_id=ping.message_id), message_id=ping.message_id)
            count += 1
        if count:
            logger.info(f"FleetPingCog: re-registered {count} persistent fleet ping view(s).")

    @discord.slash_command(
        name="fleetping",
        description="Post a hidden fleet ping. Only users who click the button see the details.",
    )
    @sender_has_perm("aa_ephemeral.can_send_fleet_ping")
    async def fleetping(
        self,
        ctx,
        channel: discord.Option(discord.TextChannel, description="Channel to post the ping in"),
        message: discord.Option(str, description="Secret fleet details revealed on button click"),
    ):
        embed = discord.Embed(
            title="🔒 Click Open to view Message!",
            color=discord.Color.red(),
        )

        # Post the @everyone mention as content, embed as the body
        sent = await channel.send(
            content="@everyone",
            embed=embed,
            view=RevealView(message_id=0),
            allowed_mentions=discord.AllowedMentions(everyone=True),
        )

        FleetPing.objects.create(
            message_id=sent.id,
            secret=message,
            posted_by=ctx.author.id,
            posted_by_name=ctx.author.display_name,
        )

        final_view = RevealView(message_id=sent.id)
        await sent.edit(view=final_view)
        self.bot.add_view(final_view, message_id=sent.id)

        await ctx.respond(
            f"Fleet ping posted in {channel.mention}.",
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(FleetPingCog(bot))
