import argparse
from contrail_sandeshlibs import *

def fix_cont(ipaddr):
    ## This definition is fixed for PR1522213
    ip_list = ipaddr.split('.')
    valid_ip = '%s.%s.%s.%s' % (ip_list[3],ip_list[2],ip_list[1],ip_list[0])
    return valid_ip

def encap_chk(encap):
    if encap == 'VALID | TUNNEL_GRE ':
        return 'MPLSoGRE'
    elif encap == 'VALID | TUNNEL_MPLS_UDP ':
        return 'MPLSoUDP'
    else:
        return 'VXLAN'

def get_bum_list(host_id,vni):
    getsnh = GetContrailSandesh(hostname=host_id)
    tap_list = []
    tunnel_list = []
    vni_nhid = getsnh.get_kvxlan_list(vni)[0]['nhid']
    vrf_id = getsnh.get_knh_list(14)[0]['vrf']
    l2route_list = getsnh.get_layer2_route_list(vrf_id)
    for i in l2route_list:
        if i['mac'] == 'ff:ff:ff:ff:ff:ff':
            data = i
    
    for i in data['path_list']:
        if i['peer'] == 'Multicast':
            data = i
    
    nh_id_list = []
    nh_id_list.append(data['nh'][0]['nh_index'])
    while len(nh_id_list) > 0:
        for i in nh_id_list:
            data = getsnh.get_knh_list(i)
            if data[0]['type'] == 'COMPOSITE':
                nh_id_list.remove(i)
                for i in data[0]['component_nh']:
                    nh_id_list.append(i['nh_id'])
            elif data[0]['type'] == 'TUNNEL':
                nh_id_list.remove(i)
                tunnel_list.append(data[0])
            elif data[0]['type'] == 'ENCAP':
                nh_id_list.remove(i)
                for i in getsnh.get_itf_list():
                    if i['index'] == data[0]['encap_oif_id']:
                        tap_list.append(i)
            else:
                nh_id_list.remove(i)
    return tap_list,tunnel_list

def print_data(host_id,vni,tap_list,tunnel_list):
    data = '### Host %s VNI %s BUM Tree ###\n' % (host_id, vni)
    if len(tap_list) > 0:
        data += '---- TAP interfaces ----\n'
        for i in tap_list:
            tap_name = i['name']
            addr = i['mac_addr']
            data += 'TAP:%-15s MAC:%s\n' % (tap_name,addr)
    if len(tunnel_list) > 0:
        data += '---- Tunnel interfaces ----\n'
        for i in tunnel_list:
            tun_sip = fix_cont(i['tun_sip'])
            tun_dip = fix_cont(i['tun_dip'])
            encap = encap_chk(i['flags'])
            data +=  'SIP:%-15s DIP:%-15s Encap:%s\n' % (tun_sip,tun_dip,encap)
    return data

def main():
    parser = argparse.ArgumentParser(description='Display Mcast Tree')
    parser.add_argument('-t', '--target', dest='host_id', help='vRouter IP address')
    parser.add_argument('-v', '--vni', dest='vni', help='VXLAN Network Identifier')
    parser.add_argument('-m', '--mac', dest='mac_flag', help='Disable MAC address')
    args = parser.parse_args()
    
    host_id = args.host_id
    vni = args.vni

    tap_list,tunnel_list = get_bum_list(host_id,vni)
    pdata = print_data(host_id,vni,tap_list,tunnel_list)
    print pdata
    
if __name__ == "__main__":
    main()

