import sys
import xmltodict
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

        xml_dict = xmltodict.parse(xmldata)
        return xml_dict

    def get_path_sandesh_to_dict(self,path):
        #Return path directory info by dict
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    # start agent introspect
    def get_sg_list(self,name=''):
        #Return SgListResp by dict
        path = 'Snh_SgListReq?name=%s' % name
        return self.get_path_sandesh_to_dict(path)

    def get_vn_list(self,name=''):
        #Return VnListResp by dict
        path = 'Snh_VnListReq?name=%s' % name
        return self.get_path_sandesh_to_dict(path)

    def get_vm_list(self,name=''):
        #Return VmListResp by dict
        path = 'Snh_VmListReq?uuid=%s' % name
        return self.get_path_sandesh_to_dict(path)

    def get_nh_list(self):
        #Return NhListResp by dict
        path = 'Snh_NhListReq'
        return self.get_path_sandesh_to_dict(path)

    def get_vrf_list(self,name=''):
        #Return VrfListResp by dict
        path = 'Snh_VrfListReq?name=%s' % name
        return self.get_path_sandesh_to_dict(path)

    def get_inet4_uc_route(self, vrf_index='',src_ip='',prefix_len='',stale=''):
        #Return Inet4UcRouteResp by dict
        path = 'Snh_Inet4UcRouteReq?vrf_index=%s&src_ip=%s&prefix_len=%s&stale=%s' % (vrf_index,src_ip,prefix_len,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_inet6_uc_route(self, vrf_index='',src_ip='',prefix_len='',stale=''):
        #Return Inet6UcRouteResp by dict
        path = 'Snh_Inet6UcRouteReq?vrf_index=%s&src_ip=%s&prefix_len=%s&stale=%s' % (vrf_index,src_ip,prefix_len,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_inet4_mc_route(self, vrf_index='',stale=''):
        #Return Inet4McRouteResp by dict
        path = 'Snh_Inet4McRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=%s' % (vrf_index,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_layer2_route(self, vrf_index='',mac='',stale=''):
        #Return Layer2RouteResp by dict
        path = 'Snh_Layer2RouteReq?vrf_index=%s&mac=%s&stale=%s' % (vrf_index,mac,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_bridge_route(self, vrf_index='',mac='',stale=''):
        #Return BridgeRouteReq by dict
        path = 'Snh_BridgeRouteReq?vrf_index=%s&mac=%s&stale=%s' % (vrf_index,mac,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_evpn_route(self, vrf_index='',mac='',stale=''):
        #Return EvpnRouteResp by dict
        path = 'Snh_EvpnRouteReq?vrf_index=%s&mac=%s&stale=%s' % (vrf_index,mac,stale)
        return self.get_path_sandesh_to_dict(path)

    def get_itf(self,name='',_type='',uuid='',vn='',mac='',ipv4_address='',ipv6_address='',parent_uuid='',ip_active='',ip6_active='',l2_active=''):
        #Return ItfResp by dict
        path = 'Snh_ItfReq?name=%s&type=%s&uuid=%s&vn=%s&mac=%s&ipv4_address=%s&ipv6_address=%s&parent_uuid=%s&ip_active=%s&ip6_active=%s&l2_active=%s' % (name,_type,uuid,vn,mac,ipv4_address,ipv6_address,parent_uuid,ip_active,ip6_active,l2_active)
        return self.get_path_sandesh_to_dict(path)

    def get_mpls(self):
        #Return MplsResp by dict
        path = 'Snh_MplsReq'
        return self.get_path_sandesh_to_dict(path)

    def get_vrf_assign(self,uuid=''):
        #Return VrfAssignReq by dict
        path = 'Snh_VrfAssignReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_mirror_entry(self):
        #Return MirrorEntryResp by dict
        path = 'Snh_MirrorEntryReq'
        return self.get_path_sandesh_to_dict(path)

    def get_link_local_service(self):
        #Return LinkLocalServiceResp by dict
        path = 'Snh_LinkLocalServiceInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_load_balancer(self,uuid=''):
        #Return LoadBalancerResp by dict
        path = 'Snh_LoadBalancerReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_acl(self,uuid=''):
        #Return AclResp by dict
        path = 'Snh_AclReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_acl_flow(self,uuid=''):
        #Return AclFlowResp by dict
        path = 'Snh_AclFlowReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_next_acl_flow_count(self,iteration_key=''):
        #Return AclFlowCountResp by dict
        path = 'Snh_NextAclFlowCountReq?iteration_key=%s' % iteration_key
        return self.get_path_sandesh_to_dict(path)

    def get_acl_flow_count(self,uuid=''):
        #Return AclFlowCountResp by dict
        path = 'Snh_AclFlowCountReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_vxlan(self):
        #Return VxLanResp by dict
        path = 'Snh_VxLanReq'
        return self.get_path_sandesh_to_dict(path)

    def get_vxlan_config(self,vxlan_id='',vn='',active=''):
        #Return VxLanConfigResp by dict
        path = 'Snh_VxLanConfigReq?vxlan_id=%s&vn=%s&active=%s' % (vxlan_id,vn,active)
        return self.get_path_sandesh_to_dict(path)

    def get_service_instance(self,uuid=''):
        #Return ServiceInstanceResp by dict
        path = 'Snh_ServiceInstanceReq?uuid=%s' % uuid
        return self.get_path_sandesh_to_dict(path)

    def get_mirror_cfg_vn_info(self,vn_name=''):
        #Return MirrorCfgVnInfoResp by dict
        path = 'Snh_MirrorCfgVnInfoReq?vn_name=%s' % vn_name
        return self.get_path_sandesh_to_dict(path)

    def get_intf_mirror_cfg_display(self,handle=''):
        #Return IntfMirrorCfgDisplayResp by dict
        path = 'Snh_IntfMirrorCfgDisplayReq?handle=%s' % handle
        return self.get_path_sandesh_to_dict(path)

    def get_unresolved_nh_list(self):
        #Return UnresolvedNhListResp by dict
        path = 'Snh_UnresolvedNH'
        return self.get_path_sandesh_to_dict(path)

    def get_unresolved_inet4_uc_route_list(self):
        #Return UnresolvedInet4UcRouteResp by dict
        path = 'Snh_UnresolvedRoute'
        return self.get_path_sandesh_to_dict(path)

    def get_sandesh_device_list(self,name=''):
        #Return SandeshDeviceListResp by dict
        path = 'Snh_SandeshDeviceReq?name=%s' % name
        return self.get_path_sandesh_to_dict(path)

    def get_sandesh_physical_device_vn_list(self,device='',vn=''):
        #Return SandeshPhysicalDeviceVnListResp by dict
        path = 'Snh_SandeshPhysicalDeviceVnReq?device=%s&vn=%s' % (device,vn)
        return self.get_path_sandesh_to_dict(path)

    def get_sandesh_config_physical_device_vn_list(self,device=''):
        #Return SandeshPhysicalDeviceVnListResp by dict
        path = 'Snh_SandeshConfigPhysicalDeviceVnReq?device=%s' % device
        return self.get_path_sandesh_to_dict(path)

    def get_vrouter_object_limit(self):
        #Return VrouterObjectLimitsResp by dict
        path = 'Snh_VrouterObjectLimitsReq'
        return self.get_path_sandesh_to_dict(path)
    # end agent introspect

    # start kstate introspect
    def get_kinterface(self,if_id=''):
        #Return KInterfaceResp by dict
        path = 'Snh_KInterfaceReq?if_id=%s' % if_id
        return self.get_path_sandesh_to_dict(path)

    def get_kroute(self, vrf_id=''):
        #Return KRouteReq by dict
        #path = 'Snh_KRouteReq?vrf_id=%s' % vrf_id
        #return self.get_path_sandesh_to_dict(path)
        return 'KrouteReq has issue so that this function is closed'

    def get_knh(self,nh_id=''):
        #Return KNHResp by dict
        path = 'Snh_KNHReq?nh_id=%s' % nh_id
        return self.get_path_sandesh_to_dict(path)

    def get_kmpls(self,mpls_label=''):
        #Return KMPLSResp by dict
        path = 'Snh_KMplsReq?mpls_label=%s' % mpls_label
        return self.get_path_sandesh_to_dict(path)

    def get_kmirror(self,mirror_id=''):
        #Return KMirrorResp by dict
        path = 'Snh_KMirrorReq?mirror_id=%s' % mirror_id
        return self.get_path_sandesh_to_dict(path)

    def get_next_kflow(self,flow_handle=''):
        #Return NextKFlowResp by dict
        path = 'Snh_NextKFlowReq?flow_handle=%s' % flow_handle
        return self.get_path_sandesh_to_dict(path)

    def get_kflow(self,flow_idx=''):
        #Return KFlowResp by dict
        path = 'Snh_KFlowReq?flow_idx=%s' % flow_idx
        return self.get_path_sandesh_to_dict(path)

    def get_kvxlan(self,vxlan_label=''):
        #Return KVxlanResp by dict
        path = 'Snh_KVxLanReq?vxlan_label=%s' % vxlan_label
        return self.get_path_sandesh_to_dict(path)

    def get_kvrf_assign(self,vif_index=''):
        #Return KVrfAssignResp by dict
        path = 'Snh_KVrfAssignReq?vif_index=%s' % vif_index
        return self.get_path_sandesh_to_dict(path)

    def get_kvrf_stats(self,vrf_index=''):
        #Return KVrfStatsResp by dict
        path = 'Snh_KVrfStatsReq?vrf_index=%s' % vrf_index
        return self.get_path_sandesh_to_dict(path)

    def get_kdrop_stats(self):
        #Return KDropStatsResp by dict
        path = 'Snh_KDropStatsReq'
        return self.get_path_sandesh_to_dict(path)
    # end kstate introspect

    # start ovsdb introspect
    def get_ovsdb_client(self):
        #Return OvsdbClientResp by dict
        path = 'Snh_OvsdbClientReq'
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_physical_switch(self,session_remote_ip='',session_remote_port=''):
        #Return OvsdbPhysicalSwitchResp by dict
        path = 'Snh_OvsdbPhysicalSwitchReq?session_remote_ip=%s&session_remote_port=%s' % (session_remote_ip,session_remote_port)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_physical_port(self,session_remote_ip='',session_remote_port='',name=''):
        #Return OvsdbPhysicalPortResp by dict
        path = 'Snh_OvsdbPhysicalPortReq?session_remote_ip=%s&session_remote_port=%s&name=%s' % (session_remote_ip,session_remote_port,name)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_logical_switch(self,session_remote_ip='',session_remote_port='',name=''):
        #Return OvsdbLogicalSwitchResp by dict
        path = 'Snh_OvsdbLogicalSwitchReq?session_remote_ip=%s&session_remote_port=%s&name=%s' % (session_remote_ip,session_remote_port,name)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_vlan_port_binding(self,session_remote_ip='',session_remote_port='',physical_port=''):
        #Return OvsdbVlanPortBindingResp by dict
        path = 'Snh_OvsdbVlanPortBindingReq?session_remote_ip=%s&session_remote_port=%s&physical_port=%s' % (session_remote_ip,session_remote_port,physical_port)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_unicast_mac_local(self,session_remote_ip='',session_remote_port='',logical_switch='',mac=''):
        #Return OvsdbUnicastMacLocalResp by dict
        path = 'Snh_OvsdbUnicastMacLocalReq?session_remote_ip=%s&session_remote_port=%s&logical_switch=%s&mac=%s' % (session_remote_ip,session_remote_port,logical_switch,mac)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_vrf(self,session_remote_ip='',session_remote_port='',logical_switch='',mac=''):
        #Return OvsdbVrfResp by dict
        path = 'Snh_OvsdbVrfReq?session_remote_ip=%s&session_remote_port=%s&logical_switch=%s&mac=%s' % (session_remote_ip,session_remote_port,logical_switch,mac)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_unicast_mac_remote(self,session_remote_ip='',session_remote_port='',logical_switch='',mac=''):
        #Return OvsdbUnicastMacRemoteResp by dict
        path = 'Snh_OvsdbUnicastMacRemoteReq?session_remote_ip=%s&session_remote_port=%s&logical_switch=%s&mac=%s' % (session_remote_ip,session_remote_port,logical_switch,mac)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_multicast_mac_local(self,session_remote_ip='',session_remote_port='',logical_switch=''):
        #Return OvsdbMulticastMacLocalResp by dict
        path = 'Snh_OvsdbMulticastMacLocalReq?session_remote_ip=%s&session_remote_port=%s&logical_switch=%s' % (session_remote_ip,session_remote_port,logical_switch)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_ha_stale_dev_vn_export(self,dev_name='',vn_uuid=''):
        #Return OvsdbHaStaleDevVnExportResp by dict
        path = 'Snh_OvsdbHaStaleDevVnExportReq?dev_name=%s&vn_uuid=%s' % (dev_name,vn_uuid)
        return self.get_path_sandesh_to_dict(path)

    def get_ovsdb_ha_stale_l2route_export(self,dev_name='',vn_uuid='',mac=''):
        #Return OvsdbHaStaleL2RouteExportReq by dict
        path = 'Snh_OvsdbHaStaleL2RouteExportReq?dev_name=%s&vn_uuid=%s&mac=%s' % (dev_name,vn_uuid,mac)
        return self.get_path_sandesh_to_dict(path)
    # end ovsdb introspect

    # start service introspect
    def get_dhcp_stats(self):
        #Return DhcpStats by dict
        path = 'Snh_DhcpInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_dhcpv6_stats(self):
        #Return Dhcpv6Stats by dict
        path = 'Snh_Dhcpv6Info'
        return self.get_path_sandesh_to_dict(path)

    def get_arp_info(self):
        #Return Snh_ArpInfo by dict
        path = 'Snh_ArpInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_dns_stats(self):
        #Return Snh_DnsStats by dict
        path = 'Snh_DnsInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_icmp_stats(self):
        #Return Snh_IcmpStats by dict
        path = 'Snh_IcmpInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_icmpv6_stats(self):
        #Return Snh_Icmpv6Stats by dict
        path = 'Snh_Icmpv6Info'
        return self.get_path_sandesh_to_dict(path)

    def get_metadata(self):
        #Return Snh_MetadataInfo by dict
        path = 'Snh_MetadataInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_show_all_info(self):
        #Return Snh_ShowAllInfo by dict
        path = 'Snh_ShowAllInfo'
        return self.get_path_sandesh_to_dict(path)

    def get_interface_arp_stats(self, index=''):
        #Return InterfaceArpStatsResponse by dict
        path = 'Snh_InterfaceArpStatsReq?interface_index=%s' % index
        return self.get_path_sandesh_to_dict(path)

    def get_pkt_trace_info(self, num_buf='', fnum_buf=''):
        #Return PktTraceInfoResponse by dict
        path = 'Snh_PktTraceInfo?num_buffers=%s&flow_num_buffers=%s' % (num_buf,fnum_buf)
        return self.get_path_sandesh_to_dict(path)

    def get_agent_dns_entries(self):
        #Return AgentDnsEntries by dict
        path = 'Snh_ShowDnsEntries'
        return self.get_path_sandesh_to_dict(path)

    def get_vm_vdns_data(self, index=''):
        #Return VmVdnsDataResponse by dict
        path = 'Snh_VmVdnsDataReq?vm_interface_index=%s' % index
        return self.get_path_sandesh_to_dict(path)

    def get_vm_vdns_list(self):
        #Return VmVdnsListResponse by dict
        path = 'Snh_VmVdnsListReq'
        return self.get_path_sandesh_to_dict(path)

    def get_fip_vdns_data(self):
        #Return FipVdnsDataResponse by dict
        path = 'Snh_FipVdnsDataReq'
        return self.get_path_sandesh_to_dict(path)

    def get_show_arp_cache(self):
        #Return ArpCacheResp by dict
        path = 'Snh_ShowArpCache'
        return self.get_path_sandesh_to_dict(path)

    def get_gw_dhcp_leases(self):
        #Return GwDhcpLeasesResponse by dict
        path = 'Snh_ShowGwDhcpLeases'
        return self.get_path_sandesh_to_dict(path)
    # end service introspect

    # start controller introspect
    def get_agent_xmpp_connection(self):
        #Return AgentXmppConnectionStatus by dict
        path = 'Snh_AgentXmppConnectionStatusReq'
        return self.get_path_sandesh_to_dict(path)

    def get_agent_dns_xmpp_connection(self):
        #Return AgentDnsXmppConnectionStatus by dict
        path = 'Snh_AgentDnsXmppConnectionStatusReq'
        return self.get_path_sandesh_to_dict(path)

    def get_discovery_xmpp_connections(self):
        #Return AgentDiscoveryXmppConnectionsResponse by dict
        path = 'Snh_AgentDiscoveryXmppConnectionsRequest'
        return self.get_path_sandesh_to_dict(path)

    def get_discovery_dns_xmpp_connections(self):
        #Return AgentDiscoveryDnsXmppConnectionsResponse by dict
        path = 'Snh_AgentDiscoveryDnsXmppConnectionsRequest'
        return self.get_path_sandesh_to_dict(path)
    # end controller introspect

    # start xmpp_server introspect
    def get_show_xmpp_server(self):
        #Return ShowXmppServerReq by dict
        path = 'Snh_ShowXmppServerReq'
        return self.get_path_sandesh_to_dict(path)

    def get_show_xmpp_connection(self):
        #Return ShowXmppConnectionResp by dict
        path = 'Snh_ShowXmppConnectionReq'
        return self.get_path_sandesh_to_dict(path)
    # end xmpp_server introspect

    def del_unused_key(self,data):
        key_list =['@type', '@identifier','@size', 'more', 'Pagination', 'OvsdbPageResp']
        for i in key_list:
            try:
                del data[i]
            except:
                pass
        return data
    
    def get_snh_dict_data(self,data):
        key = data.keys()
        if key[0].find(r'__') == 0:
            data = data[key[0]]
        data = self.del_unused_key(data)
        return_list = []
        return_dict = {}
        key = data.keys()
        for i in key:
             return_dict[i] = self.get_data(data[i])
        return return_dict

    def get_data(self,data):
        if type(data) == list:
            data_list = []
            for i in data:
                data_dict = self.get_data(i)
                data_list.append(data_dict)
            return_data = data_list
        elif type(data) != list:
            if data.has_key('@type'):
                if data['@type'] == 'sandesh':
                    sandesh_dict = {}
                    data = self.del_unused_key(data)
                    key = data.keys()
                    for i in key:
                        sandesh_dict[i] = self.get_data(data[i])
                    return_data = sandesh_dict
                elif data['@type'] == 'list':
                    data = self.del_unused_key(data)
                    key = data.keys()
                    data = data[key[0]]
                    return_data = self.get_data(data)
                elif data['@type'] == 'struct':
                    return_list = []
                    data = self.del_unused_key(data)
                    if len(data) == 0:
                        return ''
                    keys = data.keys()
                    for i in keys:
                        sdata = self.get_data(data[i])
                    return_data = sdata 
                elif data['@type'] in ['i64', 'i32', 'i16', 'u64', 'u32', 'u16', 'double', 'string', 'bool']:
                    if data.has_key('#text'):
                        return_data = data['#text']
                    else:
                        return_data = ''
            elif data.has_key('element'):
                return_data =  data['#text']
            else:
                data_dict = {}
                return_list = []
                data = self.del_unused_key(data)
                for i in data:
                     data_dict[i]= self.get_data(data[i])
                return_data = data_dict
        return return_data
    
    
    def error_msg(self, oper, msg):
        msg = '\nFaild to get %s: %s\n' % (oper,msg)
        raise ValueError(msg)
