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
            embeds = await self.generate_embed()
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
            await message.edit(embeds=embeds)
        except discord.NotFound:
            print("Message not found, creating a new one.")
            # Send the message
            await channel.send(embeds=embeds)

        # Shutdown the bot
        await client.close()

    async def generate_embed(self):
        with open("rules.yml") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        embeds = data["embeds"]

        created_embeds = []

        for embed_data in embeds:
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
            created_embeds.append(embed)

        # Limit to 10 embeds
        if len(created_embeds) > 10:
            print("Warning: More than 10 embeds found, only the first 10 will be used.")
            created_embeds = created_embeds[:10]
        return created_embeds


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(BOT_TOKEN)
