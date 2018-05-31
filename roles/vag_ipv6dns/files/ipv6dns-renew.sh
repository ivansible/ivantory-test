#!/bin/bash
#set -x

. /etc/default/ipv6dns-renew
FQDN="${HOST}.${ZONE}"
export CF_API_EMAIL=$EMAIL
export CF_API_KEY=$TOKEN

IPv6=$(ip -6 -o addr show dev eth3 | grep 'scope global' | grep -v deprecated | awk '{print $4}' | cut -d/ -f1 | head -1)
[ -z "$IPv6" ] && echo "${FQDN} ipv6 not found" && exit 1

MSG=$(cli4 --patch content="${IPv6}" "/zones/:${ZONE}/dns_records/:${FQDN}" 2>&1)
RET=$?

if [ ${RET} != 0 ] && [[ "${MSG}" =~ 'dns name not found' ]]; then
    MSG=$(cli4 --post name="${HOST}" content="${IPv6}" type=AAAA "/zones/:${ZONE}/dns_records" 2>&1)
    RET=$?
fi

[ ${RET} = 0 ] && echo "${FQDN} ipv6 OK" && exit 0
echo "${FQDN} ipv6 update error: ${MSG}" && exit ${RET}
