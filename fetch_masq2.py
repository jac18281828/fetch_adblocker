#!/usr/bin/env python

import urllib2,sys

# Choose a Steven Black Hosts file

#ad_hosts_url="https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
# fakenews gambling porn and social
ad_hosts_url='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'


# Which ip address should blocked hosts route to? 0 is best

# OpenDNS block page
# pixelserv_ip='146.112.61.104'
# not routable address
pixelserv_ip='0.0.0.0'

# local blacklist

blacklist = [
    '0.0.0.0 ad.lgappstv.com',
    '0.0.0.0 lgappstv.com',
    '0.0.0.0 yumenetworks.com',
    '0.0.0.0 cdn.spotxcdn.com', 
    '0.0.0.0 login-ds.dotomi.com',
    '0.0.0.0 yumenetworks.com',
    '0.0.0.0 smartclip.com',
    '0.0.0.0 smartshare.lgtvsdp.com',
    '0.0.0.0 ibis.lgappstv.com',
    '0.0.0.0 dclk-match.dotomi.com',
    '0.0.0.0 mopub.com',
    '0.0.0.0 mopub.net',    
    '0.0.0.0 moatads.com',
    '0.0.0.0 openx.net',
    '0.0.0.0 rubiconproject.com',
    '0.0.0.0 adnxs.com',
    '0.0.0.0 openx.com',
    '0.0.0.0 openx.net',
    '0.0.0.0 openx.com',
    '0.0.0.0 adpushup.com',
    '0.0.0.0 adpushup.net',
    '0.0.0.0 casalemedia.com',
    '0.0.0.0 casalemedia.net',    
    '0.0.0.0 contextweb.com',
    '0.0.0.0 contextweb.net',    
    '0.0.0.0 doubleclick.com',
    '0.0.0.0 doubleclick.net',
    '0.0.0.0 google-analytics.com',
    '0.0.0.0 dotomi.com',
    '0.0.0.0 pubmatic.com',
    '0.0.0.0 pubmatic.net',    
    '0.0.0.0 rubiconproject.com',
    '0.0.0.0 smaato.com',
    '0.0.0.0 smaato.net',
    '0.0.0.0 smartyads.com',
    '0.0.0.0 smartyads.net',    
    '0.0.0.0 googletagservices.com',
    '0.0.0.0 criteo.net',
    '0.0.0.0 criteo.com',    
    '0.0.0.0 tpbid.com',
    '0.0.0.0 ampproject.org',
    '0.0.0.0 pp-measurement.com',
    '0.0.0.0 advertising.com',
    '0.0.0.0 lgtvsdp.com',
    '0.0.0.0 roku.com',
    '0.0.0.0 plex.tv',
    '0.0.0.0 plexapp.com',
    '0.0.0.0 yelp.ch',
    '0.0.0.0 returnpath.net',
    '0.0.0.0 facebook.net',
    '0.0.0.0 bidswitch.net',
    '0.0.0.0 nexage.com',
    '0.0.0.0 returnpath.net',
    '0.0.0.0 conversant.com',
    '0.0.0.0 conversant.net',
    '0.0.0.0 epsilon.com',
    '0.0.0.0 subscribermail.com',
    '0.0.0.0 250analytics.com',
    '0.0.0.0 servenobid.com',
    '0.0.0.0 datadoghq.com',
    '0.0.0.0 v3qdrfxuyzwb.com',
    '0.0.0.0 forgeofempires.com',
]

# hosts which should be allowed inspite of being blacklisted
# to fix bugs in the blacklist or issues with specific providers
whitelist = [
    'nationalgeographic.com',
]

def is_excluded(host):
    for allowed in whitelist:
        if host.endswith(allowed):
            return True

    # unicode limitation for older versions of dnsmasq
    for ch in host:
        if (ord(ch) >= 128):
            return True

    return False

def read(host_url=ad_hosts_url):

    host_set = set()
    response =  urllib2.urlopen(host_url)
    host_lines = response.readlines()

    for extra in blacklist:
        host_lines.append(extra)

    for line in host_lines:
        ip_entry = line.strip()
        if len(ip_entry) > 0 and not ip_entry.startswith('#'):
            parts = ip_entry.split()
            blocked_host = parts[1]
            if not is_excluded(blocked_host):
                host_set.add(blocked_host)

    print('# dnsmasq host list generated by %s' % sys.argv[0])

    for blockhost in sorted(host_set):
        print('address=/%s/%s/' % (pixelserv_ip, blockhost))


if __name__ == '__main__':

    try:
        if len(sys.argv) > 1:
            read(sys.argv[1])
        else:
            read()
    except Exception as e:
        print('Failed. '+repr(e))
