import sys
import click
import dhcp_common

@click.command()
@click.pass_obj
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
def add_host(ctx, csv_file, hostname, mac, ip):
    """Adding reservation to host.
    """
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

    for dhcp_server in ctx.obj['dhcp_servers']:
        omapi = dhcp_common.connect_to_dhcp(dhcp_server, ctx.obj['dhcp_port'] , ctx.obj['key_name'], ctx.obj['base64key'])

        for lease in leases:
            if dhcp_common.check_host_exist(omapi, lease):
                print("Skipping, host already exist. DHCP server: " + str(dhcp_server) +" Host: " + str(lease['hostname']) +  ", ip_addr: " + str(lease['ip']) + ", mac: " + str(lease['mac']))
            else:
                # print("host: " + str(lease['hostname']) +  ", ip_addr: " + str(lease['ip']) + ", mac: " + str(lease['mac']))
                add_host_record(dhcp_server, omapi, lease)

def add_host_record(dhcp_server, omapi, host):

    omapi.add_host_supersede(str(host['ip']), str(host['mac']).replace('-', ':'), str(host['hostname']))
    print("Add soft reservation on DHCP server: " + str(dhcp_server) + " for host: " + str(host['hostname']) + ", ip_addr: " + str(host['ip']) + ", mac: " + str(host['mac']))

