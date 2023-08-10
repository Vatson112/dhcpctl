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
def del_host(ctx, csv_file, mac):
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

    for dhcp_server in ctx.obj['dhcp_servers']:
        # print(ctx.obj)
        omapi = dhcp_common.connect_to_dhcp(dhcp_server, ctx.obj['dhcp_port'], ctx.obj['key_name'], ctx.obj['base64key'])

        for lease in leases:
            if dhcp_common.check_host_exist(omapi, lease):
                # print("host: " + ", mac: " + str(lease['mac']))
                del_host_by_mac(dhcp_server, omapi, lease)
            else:
                print("Skipping, host not exist. DHCP server: " + str(dhcp_server) + " Host: "  + ", mac: " + str(lease['mac']))

def del_host_by_mac(dhcp_server, omapi, host):
    mac = str(host['mac']).replace('-', ':').lower()
    omapi.del_host(mac)
    print("Del soft reservation on DHCP server: " + str(dhcp_server) + "for mac: " +  mac)
