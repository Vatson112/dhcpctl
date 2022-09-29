import sys
import click
import dhcp_common

# dhcp_servers =[
#     "dhcp01",
#     "dhcp02"
# ]
# dhcp_port = 7911
# key_name = b"defomapi"
# base64key = b"=="

def add_soft_lease(dhcp_server, omapi, host):

    omapi.add_host_supersede(str(host['ip']), str(host['mac']).replace('-', ':'), str(host['hostname']))
    print("Add soft reservation on DHCP server: " + str(dhcp_server) + " for host: " + str(host['hostname']) + ", ip_addr: " + str(host['ip']) + ", mac: " + str(host['mac']))


@click.command()
@click.option(
    '--csv-file', '-c',
    help='CSV file with hosts in format:\n"ip";"mac";"hostname"\n"8.8.8.8";"00-00-00-00-00-00";"example"\n default = reservation.csv',
    type=click.Path()
)
@click.option(
    '--hostname', '-n',
    help='hostname or name for reservation record',
    type=str
)
@click.option(
    '--mac', '-m',
    help='MAC address for reservation record',
    type=str
)
@click.option(
    '--ip', '-i',
    help='IP address for reservation record',
    type=str
)
def add_reservation(csv_file, hostname, mac, ip):
    """Adding reservation to host.
    
    """
    csss = click.get_current_context()
    leases = []
    if csv_file:
        leases = dhcp_common.read_csv_file(csv_file, leases)
    else:
        if None in (hostname, mac, ip):
            sys.exit("Please use all hostname, mac, ip for creating reservation.")
        else:
            leases[0]['hostname'] = hostname
            leases[0]['mac'] = mac
            leases[0]['ip'] = ip


    for lease in leases:
        if not dhcp_common.validate_host(lease):
            sys.exit("Error in validation CSV file on host: " + str(lease['hostname']) +  ", ip_addr: " + str(lease['ip']) + ", mac: " + str(lease['mac']))
        else:
            lease = dhcp_common.rebuild_host(lease)  
    
    for dhcp_server in dhcp_servers:
        omapi = dhcp_common.connect_to_dhcp(dhcp_server, dhcp_port, key_name, base64key)

        for lease in leases:
            if dhcp_common.check_lease_exist(omapi, lease):
                print("Skipping, host already exist. DHCP server: " + str(dhcp_server) +" Host: " + str(lease['hostname']) +  ", ip_addr: " + str(lease['ip']) + ", mac: " + str(lease['mac']))
            else:
                # print("host: " + str(lease['hostname']) +  ", ip_addr: " + str(lease['ip']) + ", mac: " + str(lease['mac']))
                add_soft_lease(dhcp_server, omapi, lease)