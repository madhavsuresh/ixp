#!/usr/bin/python
import re
from dns import resolver,reversename,exception

mult_ip = {'bgp_to_prefix': 'Inavlid'}
f = open('./remote_peerings.txt','r')
for line in f:
    spl = line.split()
    out_list = []
    for ip in spl[3:3+3]:
        ip =  ip.strip(',[]')
        if ip not in mult_ip:
            try:
                addr = reversename.from_address(ip)
                mult_ip[ip] = str(resolver.query(addr,'PTR')[0])
            except (resolver.NXDOMAIN,exception.Timeout,resolver.NoAnswer):
                mult_ip[ip] =  'Unable to resolve'

        out_list.append(mult_ip[ip])
        print line, out_list

sortedIPs = sorted(mult_ip,key=mult_ip.get)
for ip in  sortedIPs:
    print ip,
    try:
        addr = reversename.from_address(ip)
        print str(resolver.query(addr,'PTR')[0])
    except (resolver.NXDOMAIN,exception.Timeout,resolver.NoAnswer):
        print 'Unable to resolve'
