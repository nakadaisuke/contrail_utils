import argparse
import sys
from contrail_sandeshlibs import *


def fix_cont(ipaddr):
    # This definition is fixed for PR1522213
    ip_list = ipaddr.split('.')
    valid_ip = '%s.%s.%s.%s' % (ip_list[3], ip_list[2], ip_list[1], ip_list[0])
    return valid_ip


def encap_chk(encap):
    if encap == 'VALID | TUNNEL_GRE ':
        return 'MPLSoGRE'
    elif encap == 'VALID | TUNNEL_MPLS_UDP ':
        return 'MPLSoUDP'
    else:
        return 'VXLAN'


def get_bum_list(host_id, vni):
    getsnh = GetContrailSandesh(hostname=host_id)
    tap_list = []
    tunnel_list = []
    try:
        vni_nhid = getsnh.get_kvxlan(vni)['KVxLanResp']['vxlan_list']['nhid']
    except:
        msg = "KeyError: Could not get VNI:%s" % vni
        print msg
        sys.exit(1)

    vrf_id = getsnh.get_knh(vni_nhid)['KNHResp']['nh_list']['vrf']
    l2route_list = getsnh.get_layer2_route(vrf_id)
    for i in l2route_list['BridgeRouteResp']['route_list']:
        if i['mac'] == 'ff:ff:ff:ff:ff:ff':
            data = i

    for i in data['path_list']:
        if i['peer'] == 'Multicast':
            data = i

    nh_id_list = []
    nh_id_list.append(data['nh']['nh_index'])
    while len(nh_id_list) > 0:
        for i in nh_id_list:
            data = getsnh.get_knh(i)
            data = data['KNHResp']['nh_list']
            if data['type'] == 'COMPOSITE':
                nh_id_list.remove(i)
                try:
                    if type(data['component_nh']) == list:
                        for i in data['component_nh']:
                            nh_id_list.append((i['nh_id']))
                    else:
                        nh_id_list.append((data['component_nh']['nh_id']))
                except:
                    pass
            elif data['type'] == 'TUNNEL':
                nh_id_list.remove(i)
                tunnel_list.append(data)
            elif data['type'] == 'ENCAP':
                nh_id_list.remove(i)
                for i in getsnh.get_itf()['ItfResp']['itf_list']:
                    if i['index'] == data['encap_oif_id']:
                        tap_list.append(i)
            else:
                nh_id_list.remove(i)
    return tap_list, tunnel_list


def print_data(host_id, vni, tap_list, tunnel_list, version):
    data = '### Host %s VNI %s BUM Tree ###\n' % (host_id, vni)
    if len(tap_list) > 0:
        data += '---- TAP interfaces ----\n'
        for i in tap_list:
            tap_name = i['name']
            addr = i['mac_addr']
            data += 'TAP:%-15s MAC:%s\n' % (tap_name, addr)
    if len(tunnel_list) > 0:
        data += '---- Tunnel interfaces ----\n'
        for i in tunnel_list:
            if float(version) < 2.22:
                tun_sip = fix_cont(i['tun_sip'])
                tun_dip = fix_cont(i['tun_dip'])
            else:
                tun_sip = i['tun_sip']
                tun_dip = i['tun_dip']
            encap = encap_chk(i['flags'])
            data += 'SIP:%-15s DIP:%-15s Encap:%s\n' % (
                tun_sip, tun_dip, encap)
    return data


def main():
    parser = argparse.ArgumentParser(description='Display Mcast Tree')
    parser.add_argument('-t', dest='host_id', help='vRouter IP address')
    parser.add_argument('-v', dest='vni', help='VXLAN Network Identifier')
    parser.add_argument('-m', dest='mac_flag', help='Disable MAC address')
    parser.add_argument('-c', dest='contrail_ver',
                        default=2.21, help='set_contrail_version')
    args = parser.parse_args()

    host_id = args.host_id
    vni = args.vni
    contrail_ver = args.contrail_ver

    tap_list, tunnel_list = get_bum_list(host_id, vni)
    pdata = print_data(host_id, vni, tap_list, tunnel_list, contrail_ver)
    print pdata

if __name__ == "__main__":
    main()
