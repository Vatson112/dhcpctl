import sys
import click
import dhcp_common

@click.command()
@click.pass_context
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
@click.option(
    '--ip', '-i',
    help='IP address',
    type=click.Path()
)
def del_lease(ctx, csv_file, mac,ip ):
    """Deleting lease for host.
    """
    leases = []
    if csv_file:
        leases = dhcp_common.read_csv_file(csv_file, leases)
    else:
            leases.append({})
            leases[0]['mac'] = mac
            leases[0]['ip'] = ip

    for lease in leases:
        if not dhcp_common.validate_host(lease):
            sys.exit("Error in validation CSV file on host: "  + ", mac: " + str(lease['mac']))
        else:
            lease = dhcp_common.rebuild_host(lease)

    for dhcp_server in ctx.obj['dhcp_servers']:
        # print(ctx.obj)
        omapi = dhcp_common.connect_to_dhcp(dhcp_server, ctx.obj['dhcp_port'], ctx.obj['key_name'], ctx.obj['base64key'])

        for lease in leases:
                # print("host: " + ", mac: " + str(lease['mac']))
                del_lease_by_ip(dhcp_server, omapi, lease)

def del_lease_by_mac(dhcp_server, omapi, host):
    mac = str(host['mac']).replace('-', ':').lower()
    try:
        omapi.del_lease_by_mac(mac)
    except omapi.OmapiErrorNotFound:
        print("Skipping, host not exist. DHCP server: " + str(dhcp_server) + " Host: "  + ", mac: " + mac)
    print("Del lease on DHCP server: " + str(dhcp_server) + " for mac: " +  mac)

def del_lease_by_ip(dhcp_server, omapi, host):
    ip = str(host['ip'])
    try:
        omapi.del_lease_by_ip(ip)
    except omapi.OmapiErrorNotFound:
        print("Skipping, host not exist. DHCP server: " + str(dhcp_server) + " Host: "  + ", mac: " + mac)
    print("Del lease on DHCP server: " + str(dhcp_server) + " for ip: " +  ip)