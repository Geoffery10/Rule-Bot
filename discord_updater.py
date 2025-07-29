import json
import os
import discord


# Read environment variables from GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

class MyClient(discord.Client):
    async def on_ready(self):
        with open("rules.json") as json_file:
            data = json.load(json_file)
        embed_data = data["embeds"][0]
        print(embed_data)
        
        # Fetch the channel
        channel = await self.fetch_channel(530211933215784960)
        print(f'{channel.name} channel fetched successfully!')

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
        
        # Send the message
        await channel.send(embed=embed)
        # Shutdown the bot
        await client.close()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(BOT_TOKEN)