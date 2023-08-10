import pypureomapi as oapi
import macaddress
import ipaddress
import csv
def read_csv_file(csv_file, data):
    fieldnames = ['ip', 'mac', 'hostname', 'state']
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file, delimiter = ';', doublequote = False, strict = True, fieldnames=fieldnames)
        for row in reader:
            data.append(row)

    return data

def connect_to_dhcp(ip, port, key_name, key):
    omapi = oapi.Omapi(ip, port, key_name, key)
    omapi.check_connected()

    return omapi

def check_host_exist(omapi, host):
    if 'ip' in host and host['ip'] is not None:
        ip = str(host['ip'])
        # Check lease object
        try:
            omapi.lookup_mac(ip)
            return True
        except:
            pass
        try:
            omapi.lookup_host_by_ip(ip)
            return True
        except:
            pass

    if 'mac' in host and host['mac'] is not None:
        mac = str(host['mac']).replace('-', ':')
        # Check lease object
        try:
            omapi.lookup_ip(mac)
            return True
        except:
            pass
        # Check host object
        try:
            omapi.lookup_host_host(mac)
            return True
        except:
            pass
    return False

def check_host_exist(omapi, host):
    if 'ip' in host and host['ip'] is not None:
        ip = str(host['ip'])
        # Check lease object
        try:
            omapi.lookup_mac(ip)
            return True
        except:
            pass
        try:
            omapi.lookup_host_by_ip(ip)
            return True
        except:
            pass

    if 'mac' in host and host['mac'] is not None:
        mac = str(host['mac']).replace('-', ':')
        # Check lease object
        try:
            omapi.lookup_ip(mac)
            return True
        except:
            pass
        # Check host object
        try:
            omapi.lookup_host_host(mac)
            return True
        except:
            pass
    return False

def validate_host(host):
    if 'ip' in host and host['ip'] is not None:
        try:
            host['ip'] = ipaddress.ip_address(host['ip'])
        except ValueError:
            return False

    if 'mac' in host and host['mac'] is not None:
        try:
            host['mac'] = macaddress.MAC(host['mac'])
        except ValueError:
            return False
    return True

def rebuild_host(host):
    if 'ip' in host and host['ip'] is not None:
        host['ip'] = ipaddress.ip_address(host['ip'])

    if 'mac' in host and host['mac'] is not None:
        host['mac'] = macaddress.MAC(host['mac'])

    return host
