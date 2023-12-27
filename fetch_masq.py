#!/usr/bin/env python3
import urllib.request
import sys
import traceback
import re

# Constants
AD_HOSTS_URL = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
PIXELSERV_IP = '0.0.0.0'

# Local blacklist and whitelist
blacklist = set([
    # ... (your list of blacklisted domains)
])
whitelist = set([
    # ... (your list of whitelisted domains)
])

def is_excluded(host):
    """Check if a host is excluded based on the whitelist and character checks."""
    return any(host.endswith(allowed) for allowed in whitelist) or any(ord(ch) >= 128 for ch in host)

def read(host_url=AD_HOSTS_URL):
    """Read and process hosts from a given URL, considering the blacklist and whitelist."""
    host_set = set()
    with urllib.request.urlopen(host_url) as request_stream:
        for line in request_stream:
            line = line.strip().decode()
            # remove comments
            line = re.sub(r'(?:^|\s)#.*', '', line)
            if line and line.startswith('0.0.0.0') and not line.endswith('0.0.0.0'):
                _, blocked_host = line.split()
                if not is_excluded(blocked_host):
                    host_set.add(blocked_host)

    # Adding blacklisted hosts
    host_set.update(blacklist - whitelist)

    print('# dnsmasq host list generated by {} from {}'.format(sys.argv[0], host_url))
    for blockhost in sorted(host_set):
        print('address=/{}/{}'.format(PIXELSERV_IP, blockhost))

if __name__ == '__main__':
    try:
        # read blacklist from file
        with open('blacklist.dat') as f:
            for entry in f.read().splitlines():
                blacklist.add(entry)
        
        # read whitelist from file
        with open('whitelist.dat') as f:
            for entry in f.read().splitlines():
                whitelist.add(entry)

        read(sys.argv[1] if len(sys.argv) > 1 else AD_HOSTS_URL)
    except Exception as e:
        print('Failed: {}'.format(e))
        traceback.print_exc(e)        
        sys.exit(1)
