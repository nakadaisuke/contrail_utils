#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from GetSandeshVrouter import *


parser = argparse.ArgumentParser(description='Display Mcast Tree')
parser.add_argument('-t', '--target', dest='host_id', help='vRouter IP address')
parser.add_argument('-v', '--vni', dest='vni', help='VXLAN Network Identifier')
args = parser.parse_args()

host_id = args.host_id
vni = args.vni

tap_list = []
tunnel_list = []
tap_ifls = []
tunnel_pairs = []

groute = GetSandeshVrouter(hostname=host_id)
tunnel_list, tap_list = groute.get_nh_data(vni)

def fix_cont(ipaddr):
    ## This definition is fixed for PR1522213
    ip_list = ipaddr.split('.')
    valid_ip = '%s.%s.%s.%s' % (ip_list[3],ip_list[2],ip_list[1],ip_list[0])
    return valid_ip

for i in tap_list:
    tap_ifls.append(i['itf']['#text'])

for i in tunnel_list:
    orig_data = i['KNHResp']['nh_list']['list']['KNHInfo']
    data_list = {}
    data_list['tun_sip'] = orig_data['tun_sip']['#text']
    data_list['tun_dip'] = orig_data['tun_dip']['#text']
    data_list['encap'] = orig_data['flags']['#text']
    tunnel_pairs.append(data_list)

header = '### Host %s VNI %s BUM Tree ###' % (host_id, vni)
print header
print '---- TAP interfaces ----'
for i in tap_ifls:
    print i

print '---- Tunnel interfaces ----'
for i in tunnel_pairs:
    tun_sip = fix_cont(i['tun_sip'])
    tun_dip = fix_cont(i['tun_dip'])
    print 'SIP:%s DIP:%s Encap:%s' % (tun_sip,tun_dip,i['encap'])

