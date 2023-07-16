import socket
from time import sleep
import requests
from argparse import ArgumentParser

# Create the argument parser
parser = ArgumentParser()
parser.add_argument('--test', action='store_true', help='Send message to test master')

# Parse the command-line arguments
args = parser.parse_args()

# Testing environment
if args.test:
    webhook = 'https://discord.com/api/webhooks/1129446964539424919/Vg5Xl3dPOrBnxgzha7opfyP3oYFLYRUgCqcxScmefmZZ5OETN9TT--EXrCqcPh9kVqen'
else:
    webhook = 'https://discord.com/api/webhooks/1129466798249607178/AI1t84flIUMBeY3ZEIM7ZS4Q5_6JgUN8hZKmuLVcXhlINAPYbcrdD24dbJLGiHKMj5VS'

# Fixed lists, these should be in JSON files that get parsed on startup
ping_list = ['sour_kitty', 'bepaque']
discord_ids = {'sour_kitty':'410366886321192962', 'bepaque':'183129344229638144'}

#Globals initialization
domain = 'fytocomputer.gr'
ip_str = ''
dns_Str = ''
ip1 = ''
ip2 = ''

# Intervals
alert_check_interval = 150
resolve_check_interval = 50


def send_webhook(message):
    data = {
        'content': message
    }
    response = requests.post(webhook, json=data)
    if response.status_code != 204:
        print(f"Failed to send Discord webhook: {response.text}")

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except requests.RequestException as e:
        print('Error retrieving public IP:', str(e))
        return '127.0.0.1'

def resolve_dns(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        print('Error resolving DNS:', str(e))
        return '127.0.0.1'

def create_ping_string():
    list = []
    for ping in ping_list:
        list.append('<@' + discord_ids.get(ping) + '>')
    return ', '.join(list)


def ip_alert():
    dns_ip = resolve_dns(domain)
    p_ip = get_public_ip()
    while True:
        if p_ip != dns_ip:
            message = f"**ALERT!**\n{create_ping_string()}\n\nIP address has been changed to {p_ip}"
            send_webhook(message)
            while (get_public_ip() != resolve_dns(domain)):
                sleep(resolve_check_interval)
            else:
                message = f"*Issue Resolved:* DNS record has been updated!"
                send_webhook(message)
        dns_ip = resolve_dns(domain)
        p_ip = get_public_ip()
        sleep(alert_check_interval)

ip_alert()
