import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, self_bot=True)

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='echo')
async def echo(ctx, *, message):
    """Echo a message"""
    await ctx.send(message)

@bot.command(name='help_selfbot')
async def help_selfbot(ctx):
    """Display available commands"""
    embed = discord.Embed(
        title="Self-Bot Commands",
        description="Available commands for this self-bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!echo [message]", value="Echo a message", inline=False)
    embed.add_field(name="!help_selfbot", value="Show this help message", inline=False)
    
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Don't respond to ourselves
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    
    # Process commands
    await bot.process_commands(message)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        exit(1)
    
    bot.run(TOKEN)
