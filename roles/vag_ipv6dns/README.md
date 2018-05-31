# vag_ipv6dns (local role)

This role installs a small shell script that detects IPv6 on a network inteface
and updates a [Cloudflare](https://dash.cloudflare.com/) DNS AAAA record using
[API](https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record) via
[Cloudflare CLI](https://github.com/cloudflare/python-cloudflare#cli).
Note: setting TTL is not currently possible (see [issue](https://github.com/cloudflare/python-cloudflare/issues/63)).


## Requirements

None


## Variables

Available variables are listed below, along with default values.

    ipv6dns_interface: eth0
An interface to get IPv6 address from

    ipv6dns_host: ipv6
    ipv6dns_zone: example.com
A hostname and domain (here, for FQDN of `ipv6.example.com`).
Please note that a hostname under cloudflare zone may contain a dot.

    ipv6dns_cf_email: user@example.com
    ipv6dns_cf_token: supersecret
Cloudflare authentication parameters


## Tags

- `vag_ipv6dns_all`


## Dependencies

None


## Example Playbook

    - hosts: vagrant-boxes
      roles:
         - role: vag_ipv6dns
           variable1: 1
           variable2: 2


## License

MIT

## Author Information

Created in 2018 by [IvanSible](https://github.com/ivansible)
