import yaml
import os
import discord

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: dotenv module not found.")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


class MyClient(discord.Client):
    async def on_ready(self):
        # Generate the embed
        try:
            embed = await self.generate_embed()
        except Exception as e:
            print(f"Error generating embed: {e}")
            return

        # Fetch the channel
        try:
            channel = await self.fetch_channel(530211933215784960)
            print(f'{channel.name} channel fetched successfully!')
        except discord.NotFound:
            print("Channel not found. Please check the CHANNEL_ID.")
            return

        # Update or post the message
        try:
            message = await channel.fetch_message(1399573981090283520)
            await message.edit(embed=embed)
        except discord.NotFound:
            print("Message not found, creating a new one.")
            # Send the message
            await channel.send(embed=embed)

        # Shutdown the bot
        await client.close()

    async def generate_embed(self):
        with open("rules.yml") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        embed_data = data["embeds"][0]

        embed = discord.Embed(
            title=embed_data['title'],
            description=embed_data['description'],
            color=embed_data['color'])
        try:
            embed.set_thumbnail(url=embed_data['thumbnail']['url'])
        except KeyError:
            print("Thumbnail not found in embed data.")

        # Add timestamped footer
        embed.set_footer(text='Updated as of')
        embed.timestamp = discord.utils.utcnow()

        return embed


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(BOT_TOKEN)
