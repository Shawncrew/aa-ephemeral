import logging

import discord
from discord.ext import commands

from aa_ephemeral.models import FleetPing

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
            label="Click to Reveal",
            style=discord.ButtonStyle.danger,
            emoji="🔒",
            custom_id=f"{REVEAL_BUTTON_PREFIX}{message_id}",
        )
        button.callback = self.reveal
        self.add_item(button)

    async def reveal(self, interaction: discord.Interaction):
        try:
            ping = FleetPing.objects.get(message_id=self.message_id)
            secret = ping.secret
        except FleetPing.DoesNotExist:
            secret = "Fleet ping details are no longer available."
        except Exception as e:
            logger.error(f"FleetPing lookup failed for message {self.message_id}: {e}")
            secret = "Something went wrong retrieving the fleet details."

        await interaction.response.send_message(secret, ephemeral=True)


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
    @commands.has_permissions(manage_messages=True)
    async def fleetping(
        self,
        ctx,
        channel: discord.Option(discord.TextChannel, description="Channel to post the ping in"),
        message: discord.Option(str, description="Secret fleet details revealed on button click"),
    ):
        embed = discord.Embed(
            title="🔒 Hidden Fleet Ping",
            description="Click the button below to reveal the fleet details.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Posted by {ctx.author.display_name}")

        # Post with a placeholder message_id=0; we need the sent message ID first
        sent = await channel.send(embed=embed, view=RevealView(message_id=0))

        # Persist the secret keyed by the real Discord message ID
        FleetPing.objects.create(
            message_id=sent.id,
            secret=message,
            posted_by=ctx.author.id,
        )

        # Edit the message so the button's custom_id reflects the real message ID
        final_view = RevealView(message_id=sent.id)
        await sent.edit(view=final_view)
        self.bot.add_view(final_view, message_id=sent.id)

        await ctx.respond(
            f"Fleet ping posted in {channel.mention}.",
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(FleetPingCog(bot))
