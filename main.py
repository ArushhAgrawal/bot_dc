
import discord
import os

# ========== CONFIGURATION ==========

TOKEN = os.environ["DISCORD_TOKEN"]

GUILD_ID = 1429289899172958334
STAFF_ROLE_ID = 1541951389029372036

# Put the IDs of the categories where Ticket Tool creates tickets.
TICKET_CATEGORY_IDS = {
    1539640544353976340
    # Add another category ID here if needed
}

# ===================================

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"✅ Bot online as {client.user}")
    print("👀 Waiting for new ticket channels...")


@client.event
async def on_guild_channel_create(channel):

    # Ignore channels outside your server
    if channel.guild.id != GUILD_ID:
        return

    # Ignore channels outside your ticket categories
    if channel.category_id not in TICKET_CATEGORY_IDS:
        return

    # Find the staff role
    staff_role = channel.guild.get_role(STAFF_ROLE_ID)

    if staff_role is None:
        print("❌ Staff role not found. Check STAFF_ROLE_ID.")
        return

    try:
        # Send the alert directly inside the new ticket channel
        await channel.send(
            f"{staff_role.mention} 🔔 A new ticket has been created!",
            allowed_mentions=discord.AllowedMentions(
                roles=[staff_role],
                users=False,
                everyone=False
            )
        )

        print(f"✅ Alert sent inside #{channel.name}")

    except discord.Forbidden:
        print(
            f"❌ Cannot send messages or mention staff "
            f"inside #{channel.name}. Check permissions."
        )

    except discord.HTTPException as error:
        print(f"❌ Discord API error: {error}")


if __name__ == "__main__":
    if TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE":
        raise ValueError("Paste your real Discord bot token into TOKEN first.")

    client.run(TOKEN)