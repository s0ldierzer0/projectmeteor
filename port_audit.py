import netmiko
import datetime
import csv
from netmiko import (ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException)
from netmiko.exceptions import SSHException
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetmikoTimeoutException
from tqdm import tqdm, trange
from getpass import getpass
from getpass import getuser
import stdiomask


username = stdiomask.getpass(mask='*', prompt='Enter your username: ')
password = stdiomask.getpass(mask='*', prompt='Enter user password: ')
secret = stdiomask.getpass(mask='*', prompt='Enter enable secret: ')
with open('skullsquadron_NAD.txt') as router:
    for ip in router:
        device = {
            'device_type':'cisco_ios',
            'ip': ip,
            'username':username,
            'password':password,
            'secret':secret,
            }
        

        net_connect = ConnectHandler(**device)
        net_connect.enable()
        hostname = net_connect.send_command('show run | in hostname')
        hostname = hostname.split(' ')
        hostname.pop(0)
        hostname = str(hostname)
        print('Connected to ' + hostname)
        show_mac = net_connect.send_command('show mac address-table dynamic')
        show_arp = net_connect.send_command('show arp')
        data = list((show_arp,show_mac))

        title_arp = 'Arp Entries'
        title_mac = 'CAM Table'

        title = list((title_arp,title_mac))
        with open(hostname + 'portAudit.csv', "w") as csvlogfile:
            writer = csv.writer(csvlogfile, delimiter=',')
            writer.writerow(title)
            writer.writerow(data)
        net_connect.disconnect()
