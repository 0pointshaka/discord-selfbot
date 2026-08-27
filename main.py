import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from datetime import datetime

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

@bot.command(name='export_server_logs')
async def export_server_logs(ctx, webhook_url: str = None):
    """Export server logs and send via webhook"""
    guild = ctx.guild
    
    if guild is None:
        await ctx.send("❌ This command can only be used in a server!")
        return
    
    if not webhook_url:
        await ctx.send("❌ Please provide a webhook URL!\n`!export_server_logs <webhook_url>`")
        return
    
    # Validate webhook URL
    if not webhook_url.startswith('https://discord.com/api/webhooks/'):
        await ctx.send("❌ Invalid webhook URL!")
        return
    
    status_msg = await ctx.send("📊 Exporting server logs...")
    
    try:
        # Collect server information
        server_info = {
            "Server Name": guild.name,
            "Server ID": guild.id,
            "Owner": str(guild.owner),
            "Members": guild.member_count,
            "Channels": len(guild.channels),
            "Roles": len(guild.roles),
            "Export Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Collect channel information
        channels_info = []
        for channel in guild.channels:
            channel_data = {
                "Name": channel.name,
                "Type": str(channel.type),
                "ID": channel.id,
                "Created At": channel.created_at.strftime("%Y-%m-%d %H:%M:%S") if channel.created_at else "Unknown"
            }
            channels_info.append(channel_data)
        
        # Collect member information
        members_info = []
        for member in guild.members[:50]:  # Limit to 50 members
            member_data = {
                "Username": str(member),
                "ID": member.id,
                "Joined At": member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Unknown",
                "Roles": ", ".join([role.name for role in member.roles if role.name != "@everyone"])
            }
            members_info.append(member_data)
        
        # Collect role information
        roles_info = []
        for role in guild.roles[:20]:  # Limit to 20 roles
            role_data = {
                "Name": role.name,
                "ID": role.id,
                "Color": str(role.color),
                "Members": len(role.members)
            }
            roles_info.append(role_data)
        
        # Create embeds for webhook
        embeds = []
        
        # Server Info Embed
        embed1 = discord.Embed(
            title="📊 Server Logs Export",
            description=f"Server: {guild.name}",
            color=discord.Color.blue()
        )
        for key, value in server_info.items():
            embed1.add_field(name=key, value=str(value), inline=True)
        embeds.append(embed1)
        
        # Channels Embed
        if channels_info:
            embed2 = discord.Embed(
                title="📁 Channels",
                color=discord.Color.green()
            )
            for i, channel in enumerate(channels_info[:10]):  # Show first 10 channels
                channel_text = f"Type: {channel['Type']}\nID: {channel['ID']}\nCreated: {channel['Created At']}"
                embed2.add_field(name=f"#{channel['Name']}", value=channel_text, inline=False)
            if len(channels_info) > 10:
                embed2.add_field(name="... and more", value=f"Total: {len(channels_info)} channels", inline=False)
            embeds.append(embed2)
        
        # Members Embed
        if members_info:
            embed3 = discord.Embed(
                title="👥 Members (Top 10)",
                color=discord.Color.purple()
            )
            for member in members_info[:10]:
                member_text = f"ID: {member['ID']}\nJoined: {member['Joined At']}\nRoles: {member['Roles'] or 'None'}"
                embed3.add_field(name=member['Username'], value=member_text, inline=False)
            if len(members_info) > 10:
                embed3.add_field(name="... and more", value=f"Total: {guild.member_count} members", inline=False)
            embeds.append(embed3)
        
        # Roles Embed
        if roles_info:
            embed4 = discord.Embed(
                title="🎭 Roles (Top 10)",
                color=discord.Color.orange()
            )
            for role in roles_info[:10]:
                role_text = f"ID: {role['ID']}\nColor: {role['Color']}\nMembers: {role['Members']}"
                embed4.add_field(name=role['Name'], value=role_text, inline=False)
            if len(roles_info) > 10:
                embed4.add_field(name="... and more", value=f"Total: {len(guild.roles)} roles", inline=False)
            embeds.append(embed4)
        
        # Send to webhook
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send(embeds=embeds)
        
        # Update status
        await status_msg.edit(content="✅ Server logs successfully exported via webhook!")
        
    except ValueError:
        await status_msg.edit(content="❌ Invalid webhook URL!")
    except Exception as e:
        await status_msg.edit(content=f"❌ Error: {str(e)}")
        print(f"Error in export_server_logs: {e}")

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
    embed.add_field(name="!export_server_logs [webhook_url]", value="Export server logs and send via webhook", inline=False)
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
