# UniFi Fetch Adblocker

[![Test](https://github.com/jac18281828/fetch_adblocker/actions/workflows/ci-image.yml/badge.svg)](https://github.com/jac18281828/fetch_adblocker/actions/workflows/ci-image.yml)

Fetch Steven Black's hosts file and convert it into `dnsmasq` `address=/domain/` rules, with local blacklist and whitelist overrides.

This repo is aimed at UniFi gateways that run `dnsmasq`. On current UniFi OS releases, `dnsmasq` is managed by `ubios-udapi-server` and the live include directory is:

`/run/dnsmasq.dhcp.conf.d/`

That directory is recreated at boot, so a persistent static copy is kept in:

`/etc/dnsmasq.d/blacklist.conf`

and a small `systemd` helper copies it back into `/run/...` during startup.

## Files

- `fetch_masq.py`: Python 3 generator.
- `blacklist.dat`: local domains to add.
- `whitelist.dat`: suffix-based allowlist.
- `bin/update_blocklist.sh`: generate the static blacklist, mirror it into the runtime directory, and reload the live `dnsmasq`.
- `bin/sync_runtime_blacklist.sh`: boot helper that restores the runtime blacklist from the static copy.
- `systemd/dnsmasq-blacklist-sync.service`: `systemd` unit for the boot helper.
- `fetch_masq2.py`: legacy Python 2 implementation for older firmware.

## How Filtering Works

1. Steven Black hosts are downloaded.
2. Non-ASCII hostnames are skipped.
3. Any hostname matching a suffix in `whitelist.dat` is skipped.
4. Domains in `blacklist.dat` are added.

The generated output is in `dnsmasq` form:

```conf
address=/example.com/
```

Blocking a parent domain also blocks its subdomains, so keep the custom lists as simple as possible.

## Modern UniFi OS Install

These steps assume the repo is copied to `/root/blacklist`.

1. Copy the repo to the gateway.
2. Make the scripts executable.

```bash
chmod 755 /root/blacklist/fetch_masq.py
chmod 755 /root/blacklist/bin/update_blocklist.sh
chmod 755 /root/blacklist/bin/sync_runtime_blacklist.sh
```

3. Generate the blacklist and install the static copy.

```bash
cd /root/blacklist
./bin/update_blocklist.sh
```

This writes:

- `/etc/dnsmasq.d/blacklist.conf`
- `/run/dnsmasq.dhcp.conf.d/blacklist.conf`

and reloads the live `dnsmasq` instance via `/run/dnsmasq-main.pid`.

4. Install the boot helper.

```bash
install -m 0755 /root/blacklist/bin/sync_runtime_blacklist.sh /root/blacklist/sync_runtime_blacklist.sh
install -m 0644 /root/blacklist/systemd/dnsmasq-blacklist-sync.service /etc/systemd/system/dnsmasq-blacklist-sync.service
systemctl daemon-reload
systemctl enable dnsmasq-blacklist-sync.service
systemctl start dnsmasq-blacklist-sync.service
```

5. Verify the helper is enabled and the runtime file matches the static file.

```bash
systemctl status dnsmasq-blacklist-sync.service --no-pager
cmp -s /etc/dnsmasq.d/blacklist.conf /run/dnsmasq.dhcp.conf.d/blacklist.conf && echo match
```

## Updating the List

Run:

```bash
cd /root/blacklist
./bin/update_blocklist.sh
```

If the generated file did not change, the script prints `Blacklist unchanged` and skips reloading `dnsmasq`.

## Why The Helper Is Needed

Older UniFi OS versions could be customized by relying on `/etc/dnsmasq.conf` and `/etc/dnsmasq.d/`.

Current UniFi OS builds start `dnsmasq` from generated runtime files such as:

- `/run/dnsmasq.dns.conf.d/main.conf`
- `/run/dnsmasq.dhcp.conf.d/blacklist.conf`

Because `/run` is a `tmpfs`, custom files placed there do not survive reboot. The helper service restores the static `/etc/dnsmasq.d/blacklist.conf` into the runtime directory during startup.

## Legacy

For older firmware, `fetch_masq2.py` is the legacy Python 2 version.
