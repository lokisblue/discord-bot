import discord
from discord.ext import commands
import asyncio
import os  # <-- مهم لقراءة التوكن من البيئة

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

voice_to_text_channels = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    if guild.id not in voice_to_text_channels:
        voice_to_text_channels[guild.id] = {}

    if after.channel is not None and before.channel != after.channel:
        voice_channel = after.channel

        if voice_channel.id not in voice_to_text_channels[guild.id]:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
            }

            for m in voice_channel.members:
                overwrites[m] = discord.PermissionOverwrite(read_messages=True)

            channel_name = f"{voice_channel.name}-chat"
            category = voice_channel.category
            text_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
            voice_to_text_channels[guild.id][voice_channel.id] = text_channel.id
        else:
            text_channel = guild.get_channel(voice_to_text_channels[guild.id][voice_channel.id])

        for m in voice_channel.members:
            await text_channel.set_permissions(m, read_messages=True, send_messages=True)

    if before.channel is not None and before.channel != after.channel:
        voice_channel = before.channel
        if voice_channel.id in voice_to_text_channels[guild.id]:
            text_channel_id = voice_to_text_channels[guild.id][voice_channel.id]
            text_channel = guild.get_channel(text_channel_id)
            await text_channel.set_permissions(member, overwrite=None)

            if len(voice_channel.members) == 0:
                await asyncio.sleep(300)
                if len(voice_channel.members) == 0:
                    await text_channel.delete()
                    del voice_to_text_channels[guild.id][voice_channel.id]

bot.run(os.getenv("MTM4NjEwMjYyODk0OTE2ODEyOA.G_jADv.2ws8Abn_MGt5VdBZVkmVqETwp5igdvJoiEQqYQ"))  # <-- تشغيل التوكن من البيئة

