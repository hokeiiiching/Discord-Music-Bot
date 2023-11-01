import discord
from discord.ext import commands
import youtube_dl
import asyncio
import nacl
import os
import yt_dlp
import ffmpeg

 
# Create a bot instance
intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)
 
# Create a class for the music bot
class MusicBot(commands.Cog):
    """
    A Discord bot that can play music from YouTube, add skip, and show the current queue of music.
    """
 
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -filter:a "volume=0.25"'
            }
 
    @commands.command(name="play")
    async def play(self, ctx, url):
        """
        Command to play music from YouTube.
 
        Parameters:
        - ctx: discord.ext.commands.Context
            The context of the command.
        - url: str
            The YouTube URL of the music to be played.
        """
 
        # Check if the bot is already playing music
        if ctx.voice_client is None:
            # Connect to the voice channel
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                return
 
        # Add the URL to the queue
        self.queue.append(url)
 
        # Check if the bot is already playing music
        if not ctx.voice_client.is_playing():
            # Play the first song in the queue
            await self.play_song(ctx)
 
    async def play_song(self, ctx):
        """
        Helper function to play the next song in the queue.
 
        Parameters:
        - ctx: discord.ext.commands.Context
            The context of the command.
        """
 
        # Check if there are songs in the queue
        if len(self.queue) > 0:
            url = self.queue.pop(0)
 
            # Download the song from YouTube
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']
 
            # Play the song
            ctx.voice_client.play(discord.FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.play_song(ctx)))
 
    @commands.command(name="skip")
    async def skip(self, ctx):
        """
        Command to skip the currently playing song.
 
        Parameters:
        - ctx: discord.ext.commands.Context
            The context of the command.
        """
 
        # Check if the bot is playing music
        if ctx.voice_client.is_playing():
            # Stop the current song
            ctx.voice_client.stop()
 
    @commands.command(name="queue")
    async def queue(self, ctx):
        """
        Command to show the current queue of music.
 
        Parameters:
        - ctx: discord.ext.commands.Context
            The context of the command.
        """
 
        # Check if there are songs in the queue
        if len(self.queue) > 0:
            # Send the queue as a message
            await ctx.send(f"Current queue: {', '.join(self.queue)}")
        else:
            await ctx.send("The queue is empty.")
 
# Add the MusicBot class as a cog to the bot
async def setup(bot):
    print("inside setup function")
    await bot.add_cog(MusicBot(bot))


asyncio.run(setup(bot))
 
# Run the bot
bot.run('MTE2OTIyNjUyODkxMjA1NjM3MA.GT0Ugb.KHgiAjl6PCFwXuDMwLozWka5uqQ0a6fyJB2djI')