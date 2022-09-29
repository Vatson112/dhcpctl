import sys
import click

import dhcp_common

# dhcp_servers =[
#     "dhcp01",
#     "dhcp02."
# ]
# dhcp_port = 7911
# key_name = b"defomapi"
# base64key = b"=="

def del_soft_lease_by_mac(dhcp_server, omapi, host):
    omapi.del_host(str(host['mac']).replace('-', ':'))
    print("Del soft reservation on DHCP server: " + str(dhcp_server) + "for mac: " +  str(host['mac']))

@click.command()
@click.option(
    '--mac', '-m',
    help='mac for reservation record',
    type=str
)
@click.option(
    '--csv-file', '-c',
    help='CSV file with hosts in format:\n"ip";"mac";"hostname"\n"8.8.8.8";"00-00-00-00-00-00";"example"\n default = reservation.csv',
    type=click.Path()
)
def del_reservation(csv_file, mac):
    """Deleting reservation for host.
    
    """
    leases = []
    if csv_file:
        leases = dhcp_common.read_csv_file(csv_file, leases)
    else:
        if mac is None:
            sys.exit("Please use  mac for deleting reservation.")
        else:
            leases.append({})
            leases[0]['mac'] = mac

    
    

    for lease in leases:
        if not dhcp_common.validate_host(lease):
            sys.exit("Error in validation CSV file on host: "  + ", mac: " + str(lease['mac']))
        else:
            lease = dhcp_common.rebuild_host(lease) 

    for dhcp_server in dhcp_servers:
        omapi = dhcp_common.connect_to_dhcp(dhcp_server, dhcp_port, key_name, base64key)

        for lease in leases:
            if dhcp_common.check_lease_exist(omapi, lease):
                # print("host: " + str(lease['hostname'])  + ", mac: " + str(lease['mac']))
                del_soft_lease_by_mac(dhcp_server, omapi, lease)
            else:
                print("Skipping, host not exist. DHCP server: " + str(dhcp_server) + " Host: "  + ", mac: " + str(lease['mac']))
            
            