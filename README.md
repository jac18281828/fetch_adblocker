# fetch_adblocker

Fetch Steven Black's host file for a dnsmasq based adblocker (Pi Hole or Unifi UDM)

1. entries with special characters are filtered because they are not supported by the older versions of dnsmasq
2. supports whitelist
3. supports localblacklist

## INSTALL

1. copy fetch_masq.py for python3
2. copy fetch_masq2.py for python2
3. chmod 755 fetch_masq.py

## RUN

` ./fetch_masq.py > /etc/dnsmasq.d/dnsmasq.adblock.conf `
