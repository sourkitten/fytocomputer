#!/usr/bin/env python3

import subprocess
import discord
from discord.ext import commands
import psutil
import socket
import requests

# Enable all intents
intents = discord.Intents.all()

# Create a bot instance with the specified intents
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    while True:
        activity = discord.Activity(type=discord.ActivityType.watching, name="/status")
        try:
            await bot.change_presence(status=discord.Status.idle, activity=activity)
            return
        except ConnectionResetError:
            print ("ConnectionResetError: Ignoring..")
            pass

@bot.command(name='status')
async def status(ctx):
    # Get system uptime using the 'uptime' command
    try:
        system_uptime = subprocess.check_output(['uptime','-p']).decode('utf-8').strip()[3:]
    except subprocess.CalledProcessError:
        system_uptime = "Unable to fetch system uptime."

    # Get system info
    cpu_utilization = psutil.cpu_percent()
    ram_info = psutil.virtual_memory()

    def get_public_ip():
        try:
            response = requests.get('https://api.ipify.org?format=json')
            data = response.json()
            public_ip = data['ip']
            return public_ip
        except requests.RequestException as e:
            print('Error retrieving public IP:', str(e))
            return '[ unavailable ]'

    # Perform DNS resolution for specified hostnames
    def resolve_host(hostname):
        try:
            ip = socket.gethostbyname(hostname)
            return ip
        except socket.gaierror:
            return "Unable to resolve"

    system_ip = get_public_ip()
    pog_ip = resolve_host('pog.fytocomputer.gr')
    fytocomputer_ip = resolve_host('fytocomputer.ddns.net')

    # Get the status of the Apache service using systemctl
    try:
        apache_status = subprocess.check_output(['systemctl', 'is-active', 'apache2.service']).decode('utf-8').strip()
        apache_status = "up" if apache_status == "active" else "down"
    except subprocess.CalledProcessError:
        apache_status = "[ unavailable ]"

    # Get the status of the Grafana service using systemctl
    try:
        grafana_status = subprocess.check_output(['systemctl', 'is-active', 'grafana-server.service']).decode('utf-8').strip()
        grafana_status = "up" if grafana_status == "active" else "down"
    except subprocess.CalledProcessError:
        grafana_status = "[ unavailable ]"

    # Get the status of the sshd service using systemctl
    try:
        sshd_status = subprocess.check_output(['systemctl', 'is-active', 'sshd.service']).decode('utf-8').strip()
        sshd_status = "up" if sshd_status == "active" else "down"
    except subprocess.CalledProcessError:
        sshd_status = "[ unavailable ]"
    
    # Get the status of the Crafty service using systemctl
    try:
        crafty_status = subprocess.check_output(['systemctl', 'is-active', 'crafty.service']).decode('utf-8').strip()
        crafty_status = "up" if crafty_status == "active" else "down"
    except subprocess.CalledProcessError:
        crafty_status = "[ unavailable ]"
    

    # Create and send the custom message
    custom_message = (
        f"```-- SYSTEM --\n"
        f"UP:  {system_uptime}\n"
        f"CPU: {cpu_utilization}%\n"
        f"RAM: {ram_info.percent}% ({(ram_info.used / (1024 ** 3)):.2f}/{int(round(ram_info.total / (1024 ** 3)))}GB)\n\n"
        f"-- WEBSERVER --\n"
        f"System IP:             {system_ip}\n"
        f"pog.fytocomputer.gr:   {pog_ip}\n"
        f"fytocomputer.ddns.net: {fytocomputer_ip}\n\n"
        f"-- SYSTEM SERVICES --\n"
        f"Apache:  {apache_status}\n"
        f"Grafana: {grafana_status}\n"
        f"sshd:    {sshd_status}\n"
        f"Crafty:  {crafty_status}```\n"
        f":sparkles: *Roses are red, violets are blue, I'm gay, and so are* **you**! :sparkles:"
    )

    await ctx.send(custom_message)

# Run the bot with your token
bot.run('MTE1NDQ1MzA2NDYyODA0Nzg5Mg.GUTwA9.cl8dk9E85sqQ6R-ovwxWf1odEuiel0fnCBJTD8')
