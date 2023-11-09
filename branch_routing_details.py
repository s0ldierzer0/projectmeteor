import netmiko
from netmiko import (ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException,)
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException
import csv
import datetime
import stdiomask
from getpass import getpass 
import sys

def extract_string(incorrect_list):
    global index 
    global check
    incorrect_list = list((incorrect_list))
    index = input('Which index (starting from 0) is not correct:')
    incorrect_list.pop(index)
    print(incorrect_list)
    check = input('Is the above list correct? (Y)es or (N)o')
    if check == 'Y':
        correct_string = str(incorrect_list)
        return correct_string
    if check == 'N':
        print(check)
        manual_string = input('Please enter the string manually:')
        return manual_string
    
def get_creds():
    global username
    global password
    username = stdiomask.getpass(mask='*', prompt='Please enter your username: ')
    password = stdiomask.getpass(mask='*', prompt='Please enter you password: ')

def get_list():
    global branch_list
    global branch_item
    branch_list = input('Please enter which branch list you would like to pull from:\n'
                        + '1: BD01\n'
                        + '2: WR01\n'
                        + '3: WR02\n'
                        + '4: ATM\n'
                        )
    if branch_list == 'BD01':
        branch_item = 'BD01'
        branch_list = 'branch_BD01_ips.txt'
    elif  branch_list == 'WR01':
        branch_item = 'WR01'
        branch_list = 'branch_WR01_ips.txt'
    elif branch_list == 'WR02':
        branch_item = 'WR02'
        branch_list = 'branch_WR02_ips.txt'
    elif branch_list == 'ATM':
        branch_item = 'ATM'
        branch_list = 'atm_router_ip.txt'
        
    else:
        print('I did not understand, please make sure to type BD01, WR01, or WR02 accurately when prompted:\n')
        get_list()
    
    return branch_list

def branch_routing_details():
    counter = 0

    now_date = datetime.datetime.now()
    now_year = str(now_date.year)
    now_day = str(now_date.day)
    now_hour = str(now_date.hour)
    now_min = str(now_date.minute)
    now_sec = str(now_date.second)
    now_month = str(now_date.month)

    now_time = (now_month + '_' + now_day + '_' + now_year + '_' + now_hour + '_' + now_min)
    with open(branch_list) as router:
        for ip in router:
            device = {
                'device_type':'cisco_ios',
                'ip':ip,
                'username':username,
                'password':password,

            }
            
            try: 
                with ConnectHandler(**device) as net_connect:
                    hostname = net_connect.send_command('show run | in hostname', expect_string='#', read_timeout=30)
                    hostname = hostname.split(' ')
                    hostname.pop(0)
                    hostname = str(hostname)
                    hostname = hostname.replace('[', '')
                    hostname = hostname.replace(']', '')
                    hostname = hostname.replace('\'', '')
                    print('Connected to ' + hostname)
                    if branch_item == 'WR01':
                        eigrp = net_connect.send_command('show run | se router eigrp', expect_string='#', read_timeout=30)
                        bgp = net_connect.send_command('show run | se router bgp', expect_string='#', read_timeout=30)
                        bgp_sum = net_connect.send_command('show ip bgp sum', expect_string='#', read_timeout=30)
                        ip_route = net_connect.send_command('show ip route', expect_string='#', read_timeout=30)
                        int_bri = net_connect.send_command('show ip int bri', expect_string='#', read_timeout=30)
                        policy_map = net_connect.send_command('show policy-map', expect_string='#', read_timeout=30)
                        bgp_log = net_connect.send_command('show log | in %BGP', expect_string='#', read_timeout=30)
                        dmvpn = net_connect.send_command('show dmvpn', expect_string='#', read_timeout=30)
                        cdp = net_connect.send_command('show cdp neighbors', expect_string='#', read_timeout=30)
                        show_inv = net_connect.send_command('show inv | in SFP|GLC-T|GLC-TE', expect_string='#', read_timeout=30)
                        show_eigrp_neighbors = net_connect.send_command('show ip eigrp neighbors', expect_string='#', read_timeout=30)
                        show_interfaces = net_connect.send_command('show interfaces | in Gig|Description:', expect_string='#', read_timeout=30)
                        ping_host = net_connect.send_command('ping 10.4.0.6', expect_string='#', read_timeout=30)
                        traceroute_host = net_connect.send_command('traceroute 10.4.0.6', expect_string='#', read_timeout=30)
                        #show_version = net_connect.send_command('show version | in cisco ISR4331/K9|Processor board ID')
                        show_version = net_connect.send_command('show version | in Software,')
                        #print(show_version)
                        #show_version = show_version.splitlines()
                        #isr4331 = show_version[1]
                        #isr4331 = isr4331.split(' ')
                        #serial_number = isr4331[3]
                        #print(serial_number)
                        #show_version = str(serial_number)
                        hostname_title = 'Hostname'
                        eigrp_title = 'EIGRP'
                        bgp_title = 'BGP'
                        bgp_sum_title = 'BGP Summary'
                        ip_route_title = 'IP Route'
                        int_bri_title = "IP Interface Brief"
                        policy_map_title = 'Policy Map'
                        bgp_log_title = 'BGP Log'
                        dmvpn_title = 'dmvpn'
                        cdp_title = 'cdp neighbors'
                        show_version_title = 'Switch or Router Serial Numbers'
                        show_inv_title = 'SFP Module Serial Numbers'
                        show_eigrp_neighbors_title = 'EIGRP Neighbors'
                        show_interfaces_title = 'Interfaces Description'
                        ping_host_title = 'Ping Results to 10.4.0.6'
                        traceroute_host_title = 'Traceroute Results to 10.4.0.6'
                        title = list((hostname_title,eigrp_title,bgp_title,bgp_sum_title,ip_route_title,int_bri_title,policy_map_title, bgp_log_title,dmvpn_title,cdp_title, show_version_title, show_inv_title, show_eigrp_neighbors_title, show_interfaces_title, ping_host_title, traceroute_host_title))
                        data = list((hostname,eigrp,bgp,bgp_sum,ip_route,int_bri,policy_map, bgp_log,dmvpn,cdp,show_version,show_inv, show_eigrp_neighbors, show_interfaces, ping_host, traceroute_host))
                        #decision = input('Is the above the expect output? (Y)es (N)o')
                        #if decision == 'Y':
                        #    isr4331 = str(isr4331)
                        #elif decision == 'N':
                        #    extract_string(isr4331)
                    elif branch_item == 'BD01':
                        eigrp = net_connect.send_command('show run | se router eigrp', expect_string='#', read_timeout=30)
                        bgp = net_connect.send_command('show run | se router bgp', expect_string='#', read_timeout=30)
                        bgp_sum = net_connect.send_command('show ip bgp sum', expect_string='#', read_timeout=30)
                        ip_route = net_connect.send_command('show ip route', expect_string='#', read_timeout=30)
                        int_bri = net_connect.send_command('show ip int bri', expect_string='#', read_timeout=30)
                        policy_map = net_connect.send_command('show policy-map', expect_string='#', read_timeout=30)
                        bgp_log = net_connect.send_command('show log | in %BGP', expect_string='#', read_timeout=30)
                        dmvpn = net_connect.send_command('show dmvpn', expect_string='#', read_timeout=30)
                        cdp = net_connect.send_command('show cdp neighbors', expect_string='#', read_timeout=30)
                        show_inv = net_connect.send_command('show inv | in SFP|GLC-T|GLC-TE')
                        show_eigrp_neighbors = net_connect.send_command('show ip eigrp neighbors')
                        show_interfaces = net_connect.send_command('show interfaces | in Gig|Description:')
                        show_version = net_connect.send_command('show version | in CAT9K')
                        show_version.splitlines()
                        hostname_title = 'Hostname'
                        eigrp_title = 'EIGRP'
                        bgp_title = 'BGP'
                        bgp_sum_title = 'BGP Summary'
                        ip_route_title = 'IP Route'
                        int_bri_title = "IP Interface Brief"
                        policy_map_title = 'Policy Map'
                        bgp_log_title = 'BGP Log'
                        dmvpn_title = 'dmvpn'
                        cdp_title = 'cdp neighbors'
                        show_version_title = 'Switch or Router Serial Numbers'
                        show_inv_title = 'SFP Module Serial Numbers'
                        show_eigrp_neighbors_title = 'EIGRP Neighbors'
                        show_interfaces_title = 'Interfaces Description'
                        title = list((hostname_title,eigrp_title,bgp_title,bgp_sum_title,ip_route_title,int_bri_title,policy_map_title, bgp_log_title,dmvpn_title,cdp_title, show_version_title, show_inv_title, show_eigrp_neighbors_title, show_interfaces_title))
                        data = list((hostname,eigrp,bgp,bgp_sum,ip_route,int_bri,policy_map, bgp_log,dmvpn,cdp,show_version,show_inv, show_eigrp_neighbors, show_interfaces))
                        #max = stack_number
                        #while max <= stack_number:
                        #    switch_stack_index = 0
                    elif branch_item == 'WR02':
                        eigrp = net_connect.send_command('show run | se router eigrp', expect_string='#', read_timeout=30)
                        bgp = net_connect.send_command('show run | se router bgp', expect_string='#', read_timeout=30)
                        bgp_sum = net_connect.send_command('show ip bgp sum', expect_string='#', read_timeout=30)
                        ip_route = net_connect.send_command('show ip route', expect_string='#', read_timeout=30)
                        int_bri = net_connect.send_command('show ip int bri', expect_string='#', read_timeout=30)
                        policy_map = net_connect.send_command('show policy-map', expect_string='#', read_timeout=30)
                        bgp_log = net_connect.send_command('show log | in %BGP', expect_string='#', read_timeout=30)
                        dmvpn = net_connect.send_command('show dmvpn', expect_string='#', read_timeout=30)
                        cdp = net_connect.send_command('show cdp neighbors', expect_string='#', read_timeout=30)
                        show_inv = net_connect.send_command('show inv | in SFP|GLC-T|GLC-TE')
                        show_eigrp_neighbors = net_connect.send_command('show ip eigrp neighbors')
                        show_interfaces = net_connect.send_command('show interfaces | in Gig|Description:')
                        show_version = net_connect.send_command('show version | in cisco ISR4331/K9|Processor board ID')
                        print(show_version)
                        show_version = show_version.splitlines()
                        isr4331 = show_version[1]
                        isr4331 = isr4331.split(' ')
                        serial_number = isr4331[3]
                        print(serial_number)
                        show_version = str(serial_number)
                        hostname_title = 'Hostname'
                        eigrp_title = 'EIGRP'
                        bgp_title = 'BGP'
                        bgp_sum_title = 'BGP Summary'
                        ip_route_title = 'IP Route'
                        int_bri_title = "IP Interface Brief"
                        policy_map_title = 'Policy Map'
                        bgp_log_title = 'BGP Log'
                        dmvpn_title = 'dmvpn'
                        cdp_title = 'cdp neighbors'
                        show_version_title = 'Switch or Router Serial Numbers'
                        show_inv_title = 'SFP Module Serial Numbers'
                        show_eigrp_neighbors_title = 'EIGRP Neighbors'
                        show_interfaces_title = 'Interfaces Description'
                        title = list((hostname_title,eigrp_title,bgp_title,bgp_sum_title,ip_route_title,int_bri_title,policy_map_title, bgp_log_title,dmvpn_title,cdp_title, show_version_title, show_inv_title, show_eigrp_neighbors_title, show_interfaces_title))
                        data = list((hostname,eigrp,bgp,bgp_sum,ip_route,int_bri,policy_map, bgp_log,dmvpn,cdp,show_version,show_inv, show_eigrp_neighbors, show_interfaces))
                        #decision = input('Is the above the expect output? (Y)es (N)o')
                        #if decision == 'Y':
                        #    isr4331 = str(isr4331)
                        #elif decision == 'N':
                        #    extract_string(isr4331)    
                    elif branch_item == 'ATM':
                        hostname_title = 'hostname'
                        eigrp_title = 'EIGRP'
                        ip_route_title = 'IP Route'
                        int_bri_title = "IP Interface Brief"
                        policy_map_title = 'Policy Map'
                        dmvpn_title = 'DMVPN Status'
                        show_eigrp_neighbors_title = 'EIGRP Neighbors'
                        show_interfaces_title = 'Interfaces Description'
                        ping_host_title = 'Ping Results to 10.4.0.6'
                        #traceroute_host_title = 'Traceroute Results to 10.4.0.6'
                        show_cell_1_RSSI_title = 'Cellular 1/0 RSSI'
                        show_cell_1_SNR_title = 'Cellular 1/0 SNR'
                        show_cell_0_RSSI_title = 'Cellular 0/0 RSSI'
                        show_cell_0_SNR_title = 'Cellular 0/0 SNR'
                        ip_route = net_connect.send_command('show ip route', expect_string='#', read_timeout=45)
                        int_bri = net_connect.send_command('show ip int bri', expect_string='#', read_timeout=45)
                        dmvpn = net_connect.send_command('show dmvpn', expect_string='#', read_timeout=45)
                        cdp = net_connect.send_command('show cdp neighbors', expect_string='#', read_timeout=45)
                        eigrp = net_connect.send_command('show run | se router eigrp', expect_string='#', read_timeout=45)
                        policy_map = net_connect.send_command('show policy-map', expect_string='#', read_timeout=45)
                        show_eigrp_neighbors = net_connect.send_command('show ip eigrp neighbors', expect_string='#', read_timeout=45)
                        show_interfaces = net_connect.send_command('show interfaces | in Gig|Description:', expect_string='#', read_timeout=45)
                        show_cell_0_RSSI =  net_connect.send_command('show cell 0/0 rad | in RSSI', expect_string='#', read_timeout=45)
                        ping_host = net_connect.send_command('ping 10.4.0.6', expect_string='#', read_timeout=45)
                        #traceroute_host = net_connect.send_command('traceroute 10.4.0.6', expect_string='#', read_timeout=45)
                        show_cell_0_RSSI = show_cell_0_RSSI.split('=')
                        show_cell_0_RSSI.pop(0)
                        show_cell_0_RSSI = str(show_cell_0_RSSI)
                        show_cell_0_RSSI = show_cell_0_RSSI.replace('[', '')
                        show_cell_0_RSSI = show_cell_0_RSSI.replace(']', '')
                        show_cell_0_RSSI = show_cell_0_RSSI.replace('\'', '')
                        show_cell_0_RSSI = show_cell_0_RSSI.replace('dBm', '')
                        print(type(show_cell_0_RSSI))
                        show_cell_0_SNR = net_connect.send_command('show cell 0/0 rad | in SNR', expect_string='#', read_timeout=45)
                        show_cell_0_SNR = show_cell_0_SNR.split('=')
                        show_cell_0_SNR.pop(0)
                        show_cell_0_SNR = str(show_cell_0_SNR)
                        show_cell_0_SNR = show_cell_0_SNR.replace('[', '')
                        show_cell_0_SNR = show_cell_0_SNR.replace(']', '')
                        show_cell_0_SNR = show_cell_0_SNR.replace('\'', '')
                        show_cell_0_SNR = show_cell_0_SNR.replace('dB', '')
                        show_cell_1_RSSI = net_connect.send_command('show cell 1/0 rad | in RSSI', expect_string='#', read_timeout=45)
                        show_cell_1_RSSI = show_cell_1_RSSI.split('=')
                        show_cell_1_RSSI.pop(0)
                        show_cell_1_RSSI = str(show_cell_1_RSSI)
                        show_cell_1_RSSI = show_cell_1_RSSI.replace('[', '')
                        show_cell_1_RSSI = show_cell_1_RSSI.replace(']', '')
                        show_cell_1_RSSI = show_cell_1_RSSI.replace('\'', '')
                        show_cell_1_RSSI = show_cell_1_RSSI.replace('dBm', '')
                        show_cell_1_SNR = net_connect.send_command('show cell 1/0 rad | in SNR', expect_string='#', read_timeout=45)
                        show_cell_1_SNR = show_cell_1_SNR.split('=')
                        show_cell_1_SNR.pop(0)
                        show_cell_1_SNR = str(show_cell_1_SNR)
                        show_cell_1_SNR = show_cell_1_SNR.replace('[', '')
                        show_cell_1_SNR = show_cell_1_SNR.replace(']', '')
                        show_cell_1_SNR = show_cell_1_SNR.replace('\'', '')
                        show_cell_1_SNR = show_cell_1_SNR.replace('dB', '')

                        title = list((hostname_title,eigrp_title,ip_route_title,int_bri_title,policy_map_title,dmvpn_title,show_eigrp_neighbors_title,show_interfaces_title,ping_host_title,show_cell_0_RSSI_title,show_cell_0_SNR_title, show_cell_1_RSSI_title, show_cell_1_SNR_title))
                        data = list((hostname,eigrp,ip_route,int_bri,policy_map,dmvpn,show_eigrp_neighbors,show_interfaces,ping_host,show_cell_0_RSSI,show_cell_0_SNR, show_cell_1_RSSI, show_cell_1_SNR))

                    #show_hardware = net_connect.send_command('show hardware | in Motherboard Serial Number|System Serial Number', expect_string='#', read_timeout=30)
                    #show_inv = net_connect.send_command('show inv | in SFP|AVC|ACW|MTC|FNS|OPM|GLC-T|GLC-TE|Cisco ISR4331 Chassis|FDO|C9300-48P|FJC|C9300-48U|FJB|NIM-2GE-CU-SFP')

                    with open(now_time + branch_item + '.csv',"a") as logfile:
                        writer = csv.writer(logfile, delimiter=',')
                        if counter == 0:
                            writer.writerow(title)
                            writer.writerow(data)
                            counter += 1
                        else:
                            writer.writerow(data)
            except NetmikoAuthenticationException as auth_exception:
                f = open("login_issues.csv", "a")
                f.write(ip + "," + hostname + "," + "Device Unreachable/SSH not enabled")
                f.write("\n")
                f.close()
                print("Timeout occurred while connecting to {hostname}:", str(timeout_exc))
                continue
            except NetmikoTimeoutException as timeout_exc:
                f = open("login_issues.csv", "a")
                f.write(ip + "," + "Device Unreachable/SSH not enabled")
                f.write("\n")
                f.close()
                print("Timeout occurred while connecting to {hostname}:", str(timeout_exc))
                continue
            except SSHException as netmiko_exc:
                f = open("login_issues.csv", "a")
                f.write(ip + "," + "SSH not enabled")
                f.write("\n")
                f.close()
                print("Netmiko SSH exception occurred:", str(netmiko_exc))
                continue
            except ValueError as exc:
                f = open("login_issues.csv", "a")
                f.write(ip + "," + "Could be SSH Enable Password issue")
                f.write("\n")
                f.close()
                print("An error occurred while connecting to {hostname}:", str(exc))
                continue
            finally:
                if net_connect is not None:
                    print('Disconnecting from ' + hostname)
                    net_connect.disconnect()

get_creds()
get_list()
branch_routing_details()
#, encoding='utf-16'

repeat = input('Would you like to repeat the program: (Y)es or (N)o:')
if repeat == 'Y':
    get_list()
    branch_routing_details()
elif repeat == 'N':
    exit()
