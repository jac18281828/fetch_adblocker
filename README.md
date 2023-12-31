# Unifi Fetch Adblocker

[![Test](https://github.com/jac18281828/fetch_adblocker/actions/workflows/ci-image.yml/badge.svg)](https://github.com/jac18281828/fetch_adblocker/actions/workflows/ci-image.yml)

## Pi-hole setup for Unifi router

Fetch Steven Black's host file for a dnsmasq based adblocker.  Either Pi Hole or Unifi UDM routers can use this method.

Steven Black’s [Hosts](https://github.com/StevenBlack/hosts) is a unified hosts file that consolidates several reputable hosts files and merges them into a single hosts file. It is a plain-text file used by all operating systems to map hostnames to IP addresses. It is used to block ads, malware, and other unwanted traffic by redirecting the traffic to a non-existent IP address.

Pi-hole is a network-wide ad blocker that runs on Raspberry Pi. It uses Steven Black’s Hosts list to block ads and other unwanted traffic. Pi-hole is a DHCP server that automatically assigns IP addresses to devices on the network and blocks ads and other unwanted traffic.  A Unifi UDM router can be used in the same way by configuring the hosts list to work with dnsmasq.

This script is designed to pull the latest version of the hosts list and convert it to dnsmasq format.

1. special characters are filtered
2. whitelist
3. blacklist

## INSTALL

1. copy fetch_masq.py for python3
2. chmod 755 fetch_masq.py

Note: fetch_mas2.py works with python2 on legacy router firmware.

## RUN

` ./fetch_masq.py > /etc/dnsmasq.d/dnsmasq.adblock.conf `

## LEGACY

'fetch_masq2.py' - legacy python 2 implementation
