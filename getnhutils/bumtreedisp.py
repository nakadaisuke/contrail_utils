#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from GetSandeshVrouter import GetSandeshVrouter


parser = argparse.ArgumentParser(description='Display Mcast Tree')
parser.add_argument('-t', '--target', dest='host_id', help='vRouter IP address')
parser.add_argument('-v', '--vni', dest='vni', help='VXLAN Network Identifier')
parser.add_argument('-m', '--mac', dest='mac_flag', help='Disable MAC address')
## MAC address needs long time to get list, if there are many interfaces in vrouter
args = parser.parse_args()

host_id = args.host_id
vni = args.vni
mac_flag = args.mac_flag

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

def encap_chk(encap):
    if encap == 'VALID | TUNNEL_GRE':
        return 'MPLSoGRE'
    elif encap == 'VALID | TUNNEL_MPLS_UDP':
        return 'MPLSoUDP'
    else:
        return 'VXLAN'

if len(tap_list) > 0:
    mac_list = groute.get_itf()
    for i in tap_list:
        data_list = {}
        data_list['tap_itf'] = i['itf']['#text']
        for h in mac_list['__ItfResp_list']['ItfResp']['itf_list']['list']['ItfSandeshData']:
            if h['name']['#text'] == i['itf']['#text']:
                 mac_addr = h['mac_addr']['#text']
                 data_list['mac_addr'] = mac_addr
                 tap_ifls.append(data_list)

for i in tunnel_list:
    orig_data = i['KNHResp']['nh_list']['list']['KNHInfo']
    data_list = {}
    data_list['tun_sip'] = orig_data['tun_sip']['#text']
    data_list['tun_dip'] = orig_data['tun_dip']['#text']
    data_list['encap'] = orig_data['flags']['#value']
    tunnel_pairs.append(data_list)

header = '### Host %s VNI %s BUM Tree ###' % (host_id, vni)
print header
if len(tap_ifls) > 0:
    print '---- TAP interfaces ----'
    for i in tap_ifls:
        tap_name = i['tap_itf']
        addr = i['mac_addr']
        print 'TAP:%-15s MAC:%s' % (tap_name,addr)

if len(tunnel_pairs) > 0:
    print '---- Tunnel interfaces ----'
    for i in tunnel_pairs:
        tun_sip = fix_cont(i['tun_sip'])
        tun_dip = fix_cont(i['tun_dip'])
        encap = encap_chk(i['encap'])
        print 'SIP:%-15s DIP:%-15s Encap:%s' % (tun_sip,tun_dip,encap)

