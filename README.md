# dhcpctl - manage isc dhcp via OMAPI

## Prototype. Do not use in production

---

## Curently supported features

1. Add reservation via command cli

```bash
./dhcpctl.py add-reservation --hostname test --mac test --ip test
```

2. Add reservation via csv file

```bash
./dhcpctl.py add-reservation -c reservation.csv
```

3. Del reservation via command cli

```bash
./dhcpctl.py del-reservation --mac test 
```

4. Del reservation via csv file

```bash
./dhcpctl.py del-reservation -c reservation.csv
```
