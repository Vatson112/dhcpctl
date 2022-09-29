#!./venv/bin/python
import click
#import click_config
import confuse
from  add_reservation import add_reservation
from del_reservation import del_reservation
# CONFIGS


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def del_soft_lease_by_mac(omapi, host):
    omapi.del_host('00:00:88:00:00:00')
    print("Del soft reservation for mac: " +  str(host['mac']))

@click.group(context_settings=CONTEXT_SETTINGS)

# @click.pass_context
@click.option(
    '--config', '-c',
    help='Config, default path - ./config.yaml',
    type=click.Path(),
    default = "config.yaml"
)
def main(config):
    init_config(config)
    pass

def init_config(config_file):
    global dhcp_servers, dhcp_port, key_name, base64key

    config = confuse.Configuration("dhcpctl", __name__)
    config.set_file(config_file)

    dhcp_servers = config['dhcp_servers'].get(list)
    dhcp_port = config['dhcp_port'].get(int)
    key_name = bytes(config['key_name'].get(str), 'utf-8')
    base64key = bytes(config['base64key'].get(str), 'utf-8')

if __name__ == "__main__":
    main.add_command(add_reservation)
    main.add_command(del_reservation)
    main()
