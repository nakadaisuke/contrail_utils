import sys
import xmldict
import urllib2
from xml.etree.ElementTree import *

class GetContrailSandesh(object):
    def __init__(self, hostname='127.0.0.1', port='8085'):
        self.hostname = hostname
        self.port = str(port)

    def get_snhdict(self, path):
        data = self.snhdict(path)
        all_path = ''
        try:
            top_key = data.keys()
            url = data[top_key[0]]['Pagination']['req']['PageReqData']['all']['#text']
            all_path = 'Snh_PageReq?x=%s' % (url)
        except:
            pass
        try:
            top_key = data.keys()
            url = data[top_key[0]]['OvsdbPageResp']['req']['OvsdbPageRespData']['all']['#text']
            all_path = 'Snh_OvsdbPageReq?x=%s' % (url)
        except:
            pass
        if all_path != '':
            data = self.snhdict(all_path)
        return data

    def snhdict(self, path):
        url = 'http://%s:%s/%s' % (self.hostname, self.port, path)
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
            xmldata = response.read()
        except:
            self.error_msg('get_xml', url)

        xml_dict = xmldict.xml_to_dict(xmldata)
        return xml_dict

    def get_sg_list(self):
        #Return SgListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.sg.0,'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vn_list(self):
        #Return VnListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vn.0,'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vm_list(self):
        #Return VmListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vm.0,'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_nh_list(self):
        #Return NhListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.nexthop.0,'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vrf_list(self):
        #Return VrfListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vrf.0,'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_inet4_uc_route(self, vrf_index):
        #Return Inet4UcRouteResp by dict
        path = 'Snh_Inet4UcRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_inet6_uc_route(self, vrf_index):
        #Return Inet6UcRouteResp by dict
        path = 'Snh_Inet6UcRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_inet4_mc_route(self, vrf_index):
        #Return Inet4McRouteResp by dict
        path = 'Snh_Inet4McRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_layer2_route(self, vrf_index):
        #Return Layer2RouteResp by dict
        path = 'Snh_Layer2RouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_bridge_route(self, vrf_index):
        #Return BridgeRouteReq by dict
        path = 'Snh_BridgeRouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_evpn_route(self, vrf_index):
        #Return EvpnRouteResp by dict
        path = 'Snh_EvpnRouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_itf(self):
        #Return ItfResp by dict
        path = 'Snh_ItfReq?name=&type=&uuid=&vn=&mac=&ipv4_address=&ipv6_address=&parent_uuid=&ip_active=&ip6_active=&l2_active='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_mpls(self):
        #Return MplsResp by dict
        path = 'Snh_MplsReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vrf_assign(self):
        #Return VrfAssignReq by dict
        path = 'Snh_VrfAssignReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_mirror_entry(self):
        #Return MirrorEntryResp by dict
        path = 'Snh_MirrorEntryReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_link_local_service(self):
        #Return LinkLocalServiceResp by dict
        path = 'Snh_LinkLocalServiceInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_load_balancer(self):
        #Return LoadBalancerResp by dict
        path = 'Snh_LoadBalancerReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_acl(self):
        #Return AclResp by dict
        path = 'Snh_AclReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_acl_flow(self):
        #Return AclFlowResp by dict
        path = 'Snh_AclFlowReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_acl_flow_count(self):
        #Return AclFlowCountResp by dict
        path = 'Snh_AclFlowCountReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_next_acl_flow_count(self):
        #Return AclFlowCountResp by dict
        path = 'Snh_NextAclFlowCountReq?iteration_key='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vxlan(self):
        #Return VxLanResp by dict
        path = 'Snh_VxLanReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vxlan_config(self):
        #Return VxLanConfigResp by dict
        path = 'Snh_VxLanConfigReq?vxlan_id=&vn=&active='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_service_instance(self):
        #Return ServiceInstanceResp by dict
        path = 'Snh_ServiceInstanceReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_mirror_cfg_vn_info(self):
        #Return MirrorCfgVnInfoResp by dict
        path = 'Snh_MirrorCfgVnInfoReq?vn_name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_intf_mirror_cfg_dsplay(self):
        #Return IntfMirrorCfgDisplayResp by dict
        path = 'Snh_IntfMirrorCfgDisplayReq?handle='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_unresolved_nh_list(self):
        #Return UnresolvedNhListResp by dict
        path = 'Snh_UnresolvedNH'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_unresolved_inet4_uc_route_list(self):
        #Return UnresolvedInet4UcRouteResp by dict
        path = 'Snh_UnresolvedRoute'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_sandesh_device_list(self):
        #Return SandeshDeviceListResp by dict
        path = 'Snh_SandeshDeviceReq?name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_sandesh_physical_device_vn_list(self):
        #Return SandeshPhysicalDeviceVnListResp by dict
        path = 'Snh_SandeshPhysicalDeviceVnReq?device=&vn='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_sandesh_config_physical_device_vn_list(self):
        #Return SandeshPhysicalDeviceVnListResp by dict
        path = 'Snh_SandeshConfigPhysicalDeviceVnReq?device='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vrouter_object_limit(self):
        #Return VrouterObjectLimitsResp by dict
        path = 'Snh_VrouterObjectLimitsReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kinterface(self):
        #Return KInterfaceResp by dict
        path = 'Snh_KInterfaceReq?if_id='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kroute(self, vrf_id):
        #Return KRouteReq by dict
        #path = 'Snh_KRouteReq?vrf_id=%s' % vrf_id
        #rsp = self.get_snhdict(path)
        #snh_data = self.get_snh_dict_data(rsp)
        #return snh_data
        return 'KrouteReq has issue so that this function is closed'

    def get_knh(self,nh_id=''):
        #Return KNHResp by dict
        path = 'Snh_KNHReq?nh_id=%s' % nh_id
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kmpls(self):
        #Return KMPLSResp by dict
        path = 'Snh_KMplsReq?mpls_label='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kmirror(self):
        #Return KMirrorResp by dict
        path = 'Snh_KMirrorReq?mirror_id='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_next_kflow(self):
        #Return NextKFlowResp by dict
        path = 'Snh_NextKFlowReq?flow_handle='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kflow(self):
        #Return KFlowResp by dict
        path = 'Snh_KFlowReq?flow_idx='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvxlan(self,vni):
        #Return KVxlanResp by dict
        path = 'Snh_KVxLanReq?vxlan_label=%s' % vni
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvrf_assign(self,vni):
        #Return KVrfAssignResp by dict
        path = 'Snh_KVrfAssignReq?vif_index='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvrf_stats(self):
        #Return KVrfStatsResp by dict
        path = 'Snh_KVrfStatsReq?vrf_index='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kdrop_stats(self):
        #Return KDropStatsResp by dict
        path = 'Snh_KDropStatsReq'
        rsp = self.get_snhdict(path)
        data = rsp['KDropStatsResp']
        snh_data = self.get_all_snh_dict(data) 
        return snh_data

    def get_ovsdb_client(self):
        #Return OvsdbClientResp by dict
        path = 'Snh_OvsdbClientReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_physical_switch(self):
        #Return OvsdbPhysicalSwitchResp by dict
        path = 'Snh_OvsdbPhysicalSwitchReq?session_remote_ip=&session_remote_port='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_physical_port(self):
        #Return OvsdbPhysicalPortResp by dict
        path = 'Snh_OvsdbPhysicalPortReq?session_remote_ip=&session_remote_port=&name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_logical_switch(self):
        #Return OvsdbLogicalSwitchResp by dict
        path = 'Snh_OvsdbLogicalSwitchReq?session_remote_ip=&session_remote_port=&name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_vlan_port_binding(self):
        #Return OvsdbVlanPortBindingResp by dict
        path = 'Snh_OvsdbVlanPortBindingReq?session_remote_ip=&session_remote_port=&physical_port='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_unicast_mac_local(self):
        #Return OvsdbUnicastMacLocalResp by dict
        path = 'Snh_OvsdbUnicastMacLocalReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_vrf(self,ls_uuid):
        #Return OvsdbVrfResp by dict
        path = 'Snh_OvsdbVrfReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_unicast_mac_remote(self,ls_uuid):
        #Return OvsdbUnicastMacRemoteResp by dict
        path = 'Snh_OvsdbUnicastMacRemoteReq?session_remote_ip=&session_remote_port=&logical_switch=%s&mac=' % ls_uuid
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_uc_mac_local_list(self,ls_uuid):
        #Return OvsdbUnicastMacLocalResp by dict
        path = 'Snh_OvsdbMulticastMacLocalReq?session_remote_ip=&session_remote_port=&logical_switch=' % ls_uuid
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_ha_stale_dev_vn_export(self,tor_name):
        #Return OvsdbHaStaleDevVnExportResp by dict
        path = 'Snh_OvsdbHaStaleDevVnExportReq?dev_name=%s&vn_uuid=' % tor_name
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_ha_stale_l2route_export(self,tor_name):
        #Return OvsdbHaStaleL2RouteExportReq by dict
        path = 'Snh_OvsdbHaStaleL2RouteExportReq?dev_name=%s&vn_uuid=&mac=' % tor_name
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_dhcp_stats(self):
        #Return DhcpStats by dict
        path = 'Snh_DhcpInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_dhcpv6_stats(self):
        #Return Dhcpv6Stats by dict
        path = 'Snh_Dhcpv6Info'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_arp_info(self):
        #Return Snh_ArpInfo by dict
        path = 'Snh_ArpInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_dns_stats(self):
        #Return Snh_DnsStats by dict
        path = 'Snh_DnsInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_icmp_stats(self):
        #Return Snh_IcmpStats by dict
        path = 'Snh_IcmpInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_icmpv6_stats(self):
        #Return Snh_Icmpv6Stats by dict
        path = 'Snh_Icmpv6Info'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_metadata(self):
        #Return Snh_MetadataInfo by dict
        path = 'Snh_MetadataInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_show_all_info(self):
        #Return Snh_ShowAllInfo by dict
        path = 'Snh_ShowAllInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_interface_arp_stats(self, index=''):
        #Return InterfaceArpStatsResponse by dict
        path = 'Snh_InterfaceArpStatsReq?interface_index=%s' % index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_pkt_trace_info(self, num_buf='', fnum_buf=''):
        #Return PktTraceInfoResponse by dict
        path = 'Snh_PktTraceInfo?num_buffers=%s&flow_num_buffers=%s' % (num_buf,fnum_buf)
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_agent_dns_entries(self):
        #Return AgentDnsEntries by dict
        path = 'Snh_ShowDnsEntries'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vm_vdns_data(self, index=''):
        #Return VmVdnsDataResponse by dict
        path = 'Snh_VmVdnsDataReq?vm_interface_index=%s' % index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vm_vdns_list(self):
        #Return VmVdnsListResponse by dict
        path = 'Snh_VmVdnsListReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_fip_vdns_data(self):
        #Return FipVdnsDataResponse by dict
        path = 'Snh_FipVdnsDataReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_show_arp_cache(self):
        #Return ArpCacheResp by dict
        path = 'Snh_ShowArpCache'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_gw_dhcp_leases(self):
        #Return GwDhcpLeasesResponse by dict
        path = 'Snh_ShowGwDhcpLeases'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_data_page(self, path):
        try:
            rsp = self.snhdict(path)
            top_key = rsp.keys()
            url = rsp[top_key[0]]['Pagination']['req']['PageReqData']['all']['#text']
            all_path = 'Snh_PageReq?x=%s' % (url)
            return all_path
        except:
            return False

    def get_ovsdb_page(self, path):
        try:
            rsp = self.snhdict(path)
            top_key = rsp.keys()
            url = rsp[top_key[0]]['OvsdbPageResp']['req']['OvsdbPageRespData']['all']['#text']
            all_path = 'Snh_OvsdbPageReq?x=%s' % (url)
            return all_path
        except:
            return False

    def get_all_snh_dict(self, root_dict, keys=None):
        all_snh_list = []
        if type(root_dict) == dict:
            value_list = root_dict
            if keys != None:
                for key in keys:
                    value_list = value_list[key]
            if type(value_list) == dict:
                data = value_list
                val_pair = self.get_key_pair(data)
                all_snh_list.append(val_pair)
            elif type(value_list) == list:
                for data in value_list:
                    val_pair = self.get_key_pair(data)
                    all_snh_list.append(val_pair)
            else:
                all_snh_list.append(value_list)

        elif type(root_dict) == list:
            for page in root_dict:
                value_list = page
                if keys != None:
                    for key in keys:
                        value_list = value_list[key]
                if type(value_list) == dict:
                    data = value_list
                    val_pair = self.get_key_pair(data)
                    all_snh_list.append(val_pair)
                elif type(value_list) == list:
                    for data in value_list:
                        val_pair = self.get_key_pair(data)
                        all_snh_list.append(val_pair)
                else:
                    all_snh_list.append(value_list)
        else:
            self.error_msg('get_all_snh_list','no valid list')

        return all_snh_list

    def get_all_snh(self, root_dict):
        tdata = root_dict
        rkeys = root_dict.keys()
        try:
            rkeys.remove('more')
        except:
            pass
        
        for i in rkeys:
            if type(tdata[i]) == dict and tdata[i].has_key('list'):
                key = tdata[i]['list'].keys()
                tkeys = ['list',key[0]]
                gdata = self.get_all_snh_dict(tdata[i], tkeys)
        all_snh_list = []

        for i in gdata:
            tdata = i
            rkeys = i.keys()
            try:
                rkeys.remove('more')
            except:
                pass
            for i in rkeys:
                if type(tdata[i]) == dict and tdata[i].has_key('list'):
                    key = tdata[i]['list'].keys()
                    tkeys = ['list',key[0]]
                    tdata[i] = self.get_all_snh_dict(tdata[i], tkeys)
            all_snh_list.append(tdata)
        
        return all_snh_list
        
    def get_key_pair(self, data):
        key_list = data.keys()
        data_pair = {}
        for key in key_list:
            if type(data[key]) == str:
                return data[key]
            if data[key].has_key('@type'):
                if data[key].has_key('#text'):
                    data_pair[key] = data[key]['#text']
                else:
                    data_pair[key] = None
            elif type(data[key]) == list or type(data[key]) == dict:
                data_pair[key] = data[key]
            else:
                data_pair[key] = None
        return data_pair

    def get_snh_list(self,data):
        snh_list = []
        for dt in data:
            if type(dt) == dict:
                for k in dt.keys():
                    if type(dt[k]) == dict and (dt[k]).has_key('@type') ==True:
                        try:
                            dt[k] = dt[k]['#text']
                        except:
                            dt[k] = None
                    elif type(dt[k]) == dict:
                        dt[k] = self.get_data(dt[k])
                        dt[k] = self.get_snh_list(dt[k])
                    elif type(dt[k]) == list:
                        dt_list = []
                        for idt in dt[k]:
                            if type(idt) == dict:
                                for ik in idt.keys():
                                    if type(idt[ik]) == dict and (idt[ik]).has_key('@type') == True:
                                        try:
                                            idt[ik] = idt[ik]['#text']
                                        except:
                                            idt[ik] = None
                                    elif type(idt[ik]) == dict:
                                        idt[ik] = self.get_data(idt[ik])
                                        idt[ik] = self.get_list(idt[ik])
                            dt_list.append(idt)
                        dt[k] = dt_list
            snh_list.append(dt)
        return snh_list
     
    def get_snh_dict_data(self,data):
        key = data.keys()
        if key[0].find(r'__') == 0:
            data = data[key[0]]
            key = data.keys()

        try:
            key.remove('Pagination')
        except:
            pass
        try:
            key.remove('OvsdbPageResp')
        except:
            pass

        rdata = {}
        for k in key:
            if type(data[k]) == dict:
                rdata[k] = self.get_nest_data(data[k])
            elif type(data[k]) == list:
                all_data = {}
                for idata in data[k]:
                    ndata = self.get_nest_data(idata)
                    all_data.update(ndata)
                rdata[k] = all_data

        return rdata


    def get_nest_data(self,data):
        try:
            del data['more']
        except:
            pass

        all_rdata = {}
        for key in data:
            try:
                if data[key].has_key('@type'):
                   ddict = {} 
                   try:
                       ddict[key] = data[key]['#text']
                       all_rdata[key] = ddict[key]
                   except:
                       pass
                else:   
                    rdata = self.get_data(data[key])
                    if type(rdata) == dict:
                        if rdata.has_key('element'):
                            rdata = rdata['element']
                    elif type(rdata[0]) != dict:
                        rdata = None
                    else:
                        rdata = self.get_snh_list(rdata)
                    all_rdata[key] = rdata
            except:
                pass
    
        return all_rdata
    
    def get_data(self,data):
        while True:
            key = data.keys()
            if len(key) != 1:
               data = self.get_nest_data(data)
               return data
            elif type(data[key[0]]) == str:
                break
            elif type(data[key[0]]) == dict:
                if data[key[0]].has_key('element') == True:
                    data = data[key[0]]
                    return data
            data = data[key[0]]
            if key[0].islower() == False:
                break
        data = self.get_all_snh_dict(data)
        return data
    
    def error_msg(self, oper, msg):
        msg = '\nFaild to get %s: %s\n' % (oper,msg)
        raise ValueError(msg)
