import netmiko
from netmiko import ConnectHandler
import csv
import datetime
from getpass import getpass

now_date = datetime.datetime.now()
now_year = str(now_date.year)
now_day = str(now_date.day)
now_hour = now_date.hour
#if now_hour > 12:

now_hour = str(now_date.hour)
now_min = str(now_date.minute)
now_sec = str(now_date.second)
now_month = str(now_date.month)

now_time = (now_month + '_' + now_day + '_' + now_year + '_' + now_hour + '_' + now_min)


def decision(second_verify):
    if second_verify == 'Y':
        return second_verify
    else:  
        print('Close program and re-enter IP address if hostname ' + hostname + ' is inaccurate.\n')
        corrected_asn = input('If hostname ' + hostname + ' is accurate, please enter proper ASN:')
        return corrected_asn


counter = 0
counter_ports = 0

def get_creds():
    global username
    global password
    username = input('Please enter your username: ')
    password = getpass('Please enter you password: ')


get_creds()


def get_ip():
    global ip
    ip = input('Enter the IP address for the device in question:')

    
get_ip()

#with open('ipaddress.txt') as device:
    #for ip in device:
router = {
    'device_type':'cisco_ios',
    'ip':ip,
    'username':username,
    'password':password,
        }



net_connect = ConnectHandler(**router)
net_connect.enable()

hostname = net_connect.send_command('show run | in hostname')

hostname = hostname.split(' ')
hostname.pop(0)
hostname = str(hostname)
hostname = hostname.replace('[',' ')
hostname = hostname.replace(']',' ')
hostname = hostname.replace('\'',' ')
hostname = hostname.replace(' ', '')

bgp = net_connect.send_command('show run | in router bgp')
bgp = bgp.split(' ')
bgp_asn = bgp[2]
bgp_neighbor = net_connect.send_command('show ip bgp neighbors | in BGP neighbor is')
bgp_neighbor = bgp_neighbor.replace('BGP neighbor is ',' ')
bgp_neighbor = bgp_neighbor.replace('\'', ' ')
bgp_neighbor = bgp_neighbor.split(',')
bgp_neighbor.pop(2)
#print(bgp_neighbor[0])
#print(bgp_neighbor[1])
bgp_neighbor_ip = bgp_neighbor[0]
bgp_neighbor_asn = bgp_neighbor[1]

print(hostname)
print(bgp_asn)
verify = input('Are the hostname and ASN local accurate? (Y)es or (N)o:')
capital_Y = 'Y'
y = 'y'
Yes = 'Yes'
yes = 'yes'
#capital_N = 'N'
#n = 'n'
#No = 'No'
#no = 'no'
print(verify)
if (verify == capital_Y):
    print('Success')
    net_connect.send_config_from_file('MPLS_Shaper_20M_to_50M_Configuration.txt')
    eigrp_50mMPLS_shaper_commands = [   'router eigrp EIGRP',
                                        'address-family ipv4 unicast autonomous-system 1',
                                        'topology base',
                                        'redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500' ]
    net_connect.send_config_set(eigrp_50mMPLS_shaper_commands)
    bgp_summary = net_connect.send_command('show ip bgp summary')
    bgp_neighbor = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip)
    bgp_neighbor_advertised_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' advertised-routes')
    bgp_neighbor_received_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' received-routes')
    bgp_neighbor_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' routes')  
    bfd_details = net_connect.send_command('show bfd neighbor details')
    policy_map_mpls_shaper_50M = net_connect.send_command('show policy-map MPLS-SHAPER-50M')
    eigrp_running_config = net_connect.send_command('show run | se router eigrp')   
elif (verify == y):
    print('Success')
    net_connect.send_config_from_file('MPLS_Shaper_20M_to_50M_Configuration.txt')
    eigrp_50mMPLS_shaper_commands = [   'router eigrp EIGRP',
                                        'address-family ipv4 unicast autonomous-system 1',
                                        'topology base',
                                        'redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500' ]
    net_connect.send_config_set(eigrp_50mMPLS_shaper_commands)
    bgp_summary = net_connect.send_command('show ip bgp summary')
    bgp_neighbor = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip)
    bgp_neighbor_advertised_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' advertised-routes')
    bgp_neighbor_received_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' received-routes')
    bgp_neighbor_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' routes')  
    bfd_details = net_connect.send_command('show bfd neighbor details')
    policy_map_mpls_shaper_50M = net_connect.send_command('show policy-map MPLS-SHAPER-50M')
    eigrp_running_config = net_connect.send_command('show run | se router eigrp')
elif (verify == Yes):
    print('Success')
    net_connect.send_config_from_file('MPLS_Shaper_20M_to_50M_Configuration.txt')
    eigrp_50mMPLS_shaper_commands = [   'router eigrp EIGRP',
                                        'address-family ipv4 unicast autonomous-system 1',
                                        'topology base',
                                        'redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500' ]
    net_connect.send_config_set(eigrp_50mMPLS_shaper_commands)
    bgp_summary = net_connect.send_command('show ip bgp summary')
    bgp_neighbor = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip)
    bgp_neighbor_advertised_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' advertised-routes')
    bgp_neighbor_received_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' received-routes')
    bgp_neighbor_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' routes')  
    bfd_details = net_connect.send_command('show bfd neighbor details') 
    policy_map_mpls_shaper_50M = net_connect.send_command('show policy-map MPLS-SHAPER-50M')
    eigrp_running_config = net_connect.send_command('show run | se router eigrp')
elif (verify == yes):
    print('Success')
    net_connect.send_config_from_file('MPLS_Shaper_20M_to_50M_Configuration.txt')
    eigrp_50mMPLS_shaper_commands = [   'router eigrp EIGRP',
                                        'address-family ipv4 unicast autonomous-system 1',
                                        'topology base',
                                        'redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500' ]
    net_connect.send_config_set(eigrp_50mMPLS_shaper_commands)
    net_connect.send_command('redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500')
    bgp_summary = net_connect.send_command('show ip bgp summary')
    bgp_neighbor = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip)
    bgp_neighbor_advertised_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' advertised-routes')
    bgp_neighbor_received_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' received-routes')
    bgp_neighbor_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' routes')  
    bfd_details = net_connect.send_command('show bfd neighbor details')
    policy_map_mpls_shaper_50M = net_connect.send_command('show policy-map MPLS-SHAPER-50M')
    eigrp_running_config = net_connect.send_command('show run | se router eigrp')
#elif (verify == capital_N):
#    verify = decision(verify)
#elif (verify == n):
#    verify = decision(verify)
#elif (verify == No):
#    verify = decision(verify)
#elif (verify == no):
#    verify = decision(verify)
else:
    print(hostname)
    print(bgp_asn)
    verify = input('Based on your response, I am not quite sure about this -_- . Are the hostname and local ASN accurate? Type Y for yes or N for no:')
    verify = decision(verify)
    bgp_asn = verify
    print(bgp_asn)
    net_connect.send_config_from_file('MPLS_Shaper_20M_to_50M_Configuration.txt')
    eigrp_50mMPLS_shaper_commands = [   'router eigrp EIGRP',
                                        'address-family ipv4 unicast autonomous-system 1',
                                        'topology base',
                                        'redistribute bgp ' + bgp_asn + 'metric 50000 10 255 1 1500' ]
    net_connect.send_config_set(eigrp_50mMPLS_shaper_commands)
    print('Success')
    bgp_summary = net_connect.send_command('show ip bgp summary')
    bgp_neighbor = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip)
    bgp_neighbor_advertised_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' advertised-routes')
    bgp_neighbor_received_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' received-routes')
    bgp_neighbor_routes = net_connect.send_command('show ip bgp neighbor ' + bgp_neighbor_ip + ' routes')  
    bfd_details = net_connect.send_command('show bfd neighbor details')
    policy_map_mpls_shaper_50M = net_connect.send_command('show policy-map MPLS-SHAPER-50M')
    eigrp_running_config = net_connect.send_command('show run | se router eigrp')
bgp_summary_title = 'BGP Summary'
bgp_neighbor_received_routes_title = 'BGP Recieved Routes'
bgp_neighbor_advertised_routes_title = 'BGP Advertised Routes'
bgp_neighbor_routes_title = 'BGP Routes'
bfd_details_title = 'BFD Details'
policy_map_mpls_shaper_50M_title = 'Policy Map MPLS Shaper 50M'
eigrp_running_config_title = 'EIGRP Running Configuration'
header = list((bgp_summary_title,bgp_neighbor_received_routes_title,bgp_neighbor_advertised_routes_title, bgp_neighbor_routes_title,bfd_details_title,policy_map_mpls_shaper_50M_title,eigrp_running_config_title))
data = list((bgp_summary,bgp_neighbor_received_routes,bgp_neighbor_advertised_routes,bgp_neighbor_routes,bfd_details,policy_map_mpls_shaper_50M,eigrp_running_config))
#print(bgp_neighbor)
#print(bgp_neighbor_ip)
#print(bgp_neighbor_asn)
with open (now_time + hostname + 'MPLS_Shaper_20M_to_50M_information.csv', "a") as csvlogfile:
        writer = csv.writer(csvlogfile, delimiter=',')
        if counter == 0:
            writer.writerow(header)
            writer.writerow(data)
            counter =+ 1
        else:
            writer.writerow(data)
net_connect.disconnect()
    