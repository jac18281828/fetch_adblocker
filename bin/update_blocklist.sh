#!/usr/bin/env /bin/bash

echo 'Fetching Blacklist'
DNSMASQ_CONF=/etc/dnsmasq.d/blacklist.conf

python3 fetch_masq.py > ${DNSMASQ_CONF}

wc -l ${DNSMASQ_CONF}
/etc/init.d/dnsmasq force-reload
