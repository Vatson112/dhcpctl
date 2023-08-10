#!./venv/bin/python
import click
import confuse
from  add_host import add_host
from del_host import del_host
from del_lease import del_lease


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option(
    '--config', '-c',
    help='Config, default path - ./config.yaml',
    type=click.Path(),
    default = "config.yaml"
)
def main(ctx, config):
    configfile = confuse.Configuration("dhcpctl", __name__)
    configfile.set_file(config)

    ctx.obj['dhcp_servers']  = configfile['dhcp_servers'].get(list)
    ctx.obj['dhcp_port'] = configfile['dhcp_port'].get(int)
    ctx.obj['key_name'] = bytes(configfile['key_name'].get(str), 'utf-8')
    ctx.obj['base64key'] = bytes(configfile['base64key'].get(str), 'utf-8')


if __name__ == "__main__":
    main.add_command(add_host)
    main.add_command(del_host)
    # main.add_command(del_lease)
    main(obj={})
