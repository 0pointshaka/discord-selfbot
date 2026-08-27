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

@bot.command(name='delete_all_channels')
async def delete_all_channels(ctx):
    """Delete all channels in the server"""
    guild = ctx.guild
    
    if guild is None:
        await ctx.send("❌ This command can only be used in a server!")
        return
    
    # Get all channels
    channels = guild.channels
    total_channels = len(channels)
    
    if total_channels == 0:
        await ctx.send("⚠️ There are no channels to delete!")
        return
    
    # Send confirmation message
    confirmation_msg = await ctx.send(
        f"⚠️ **Warning!** This will delete all {total_channels} channels in this server!\n"
        f"React with ✅ to confirm or ❌ to cancel.\n"
        f"(Automatic cancellation in 30 seconds)"
    )
    
    await confirmation_msg.add_reaction('✅')
    await confirmation_msg.add_reaction('❌')
    
    try:
        reaction, user = await bot.wait_for(
            'reaction_add',
            timeout=30.0,
            check=lambda r, u: u == ctx.author and str(r.emoji) in ['✅', '❌']
        )
        
        if str(reaction.emoji) == '❌':
            await ctx.send("❌ Cancelled!")
            return
            
    except discord.ext.commands.errors.CommandError:
        await ctx.send("⏱️ Confirmation timeout!")
        return
    
    # Delete all channels
    deleted_count = 0
    failed_count = 0
    
    status_msg = await ctx.send(f"🗑️ Deleting channels... 0/{total_channels}")
    
    for channel in channels:
        try:
            await channel.delete()
            deleted_count += 1
            
            # Update status every 5 channels
            if deleted_count % 5 == 0:
                await status_msg.edit(content=f"🗑️ Deleting channels... {deleted_count}/{total_channels}")
        except Exception as e:
            print(f"Failed to delete {channel.name}: {e}")
            failed_count += 1
    
    # Final status
    embed = discord.Embed(
        title="Channel Deletion Complete",
        description=f"Successfully deleted channels",
        color=discord.Color.green()
    )
    embed.add_field(name="Deleted", value=f"✅ {deleted_count}", inline=True)
    embed.add_field(name="Failed", value=f"❌ {failed_count}", inline=True)
    
    await status_msg.edit(content=None, embed=embed)

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
    embed.add_field(name="!delete_all_channels", value="Delete all channels in the server (requires confirmation)", inline=False)
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
