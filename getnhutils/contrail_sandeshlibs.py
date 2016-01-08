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

    def get_inet4_uc_route_list(self, vrf_index):
        #Return Inet4UcRouteResp by dict
        path = 'Snh_Inet4UcRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_inet6_uc_route_list(self, vrf_index):
        #Return Inet6UcRouteResp by dict
        path = 'Snh_Inet6UcRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_inet4_mc_route_list(self, vrf_index):
        #Return Inet4McRouteResp by dict
        path = 'Snh_Inet4McRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_layer2_route_list(self, vrf_index):
        #Return Layer2RouteResp by dict
        path = 'Snh_Layer2RouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_bridge_route_list(self, vrf_index):
        #Return BridgeRouteReq by dict
        path = 'Snh_BridgeRouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_evpn_route_list(self, vrf_index):
        #Return EvpnRouteResp by dict
        path = 'Snh_EvpnRouteReq?vrf_index=%s&mac=&stale=' % vrf_index
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_itf_list(self):
        #Return ItfResp by dict
        path = 'Snh_ItfReq?name=&type=&uuid=&vn=&mac=&ipv4_address=&ipv6_address=&parent_uuid=&ip_active=&ip6_active=&l2_active='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_mpls_list(self):
        #Return MplsResp by dict
        path = 'Snh_MplsReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vrf_assign_list(self):
        #Return VrfAssignReq by dict
        path = 'Snh_VrfAssignReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_mirror_entry_list(self):
        #Return MirrorEntryResp by dict
        path = 'Snh_MirrorEntryReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_link_local_service_list(self):
        #Return LinkLocalServiceResponse by dict
        path = 'Snh_LinkLocalServiceInfo'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_load_balancer_list(self):
        #Return LoadBalancerResp by dict
        path = 'Snh_LoadBalancerReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_acl_list(self):
        #Return AclResp by dict
        path = 'Snh_AclReq?uuid='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_acl_flow_list(self):
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

    def get_vxlan_list(self):
        #Return VxLanResp by dict
        path = 'Snh_VxLanReq'
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vxlan_config_entries(self):
        #Return VxLanConfigResp by dict
        path = 'Snh_VxLanConfigReq?vxlan_id=&vn=&active='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_service_instance_list(self):
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

    def get_kif_list(self):
        #Return KInterfaceResp by dict
        path = 'Snh_KInterfaceReq?if_id='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kroute_list(self, vrf_id):
        #Return KRouteReq by dict
        #path = 'Snh_KRouteReq?vrf_id=%s' % vrf_id
        #rsp = self.get_snhdict(path)
        #snh_data = self.get_snh_dict_data(rsp)
        #return snh_data
        return 'KrouteReq has issue so that this function is closed'

    def get_knh_list(self,nh_id=''):
        #Return KNHResp by dict
        path = 'Snh_KNHReq?nh_id=%s' % nh_id
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kmpls_list(self):
        #Return KMPLSResp by dict
        path = 'Snh_KMplsReq?mpls_label='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kmirror_list(self):
        #Return KMirrorResp by dict
        path = 'Snh_KMirrorReq?mirror_id='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_next_kflow_list(self):
        #Return NextKFlowResp by dict
        path = 'Snh_NextKFlowReq?flow_handle='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kflow_list(self):
        #Return KFlowResp by dict
        path = 'Snh_KFlowReq?flow_idx='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvxlan_list(self,vni):
        #Return KVxlanResp by dict
        path = 'Snh_KVxLanReq?vxlan_label=%s' % vni
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvrf_assign_list(self,vni):
        #Return KVrfAssignResp by dict
        path = 'Snh_KVrfAssignReq?vif_index='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_kvrf_stats_list(self):
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

    def get_pswitch(self):
        #Return OvsdbPhysicalSwitchResp by dict
        path = 'Snh_OvsdbPhysicalSwitchReq?session_remote_ip=&session_remote_port='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_pport_list(self):
        #Return OvsdbPhysicalPortResp by dict
        path = 'Snh_OvsdbPhysicalPortReq?session_remote_ip=&session_remote_port=&name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_lswitch(self):
        #Return OvsdbLogicalSwitchResp by dict
        path = 'Snh_OvsdbLogicalSwitchReq?session_remote_ip=&session_remote_port=&name='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_vlan_port_binding_list(self):
        #Return OvsdbVlanPortBindingResp by dict
        path = 'Snh_OvsdbVlanPortBindingReq?session_remote_ip=&session_remote_port=&physical_port='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_uc_mac_local_list(self):
        #Return OvsdbUnicastMacLocalResp by dict
        path = 'Snh_OvsdbUnicastMacLocalReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ovsdb_vrf_list(self,ls_uuid):
        #Return OvsdbVrfResp by dict
        path = 'Snh_OvsdbVrfReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_uc_mac_remote_list(self,ls_uuid):
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

    def get_ha_stale_dev_vn_export(self,tor_name):
        #Return OvsdbHaStaleDevVnExportResp by dict
        path = 'Snh_OvsdbHaStaleDevVnExportReq?dev_name=%s&vn_uuid=' % tor_name
        rsp = self.get_snhdict(path)
        snh_data = self.get_snh_dict_data(rsp)
        return snh_data

    def get_ha_stale_l2route_export(self,tor_name):
        #Return OvsdbHaStaleL2RouteExportReq by dict
        path = 'Snh_OvsdbHaStaleL2RouteExportReq?dev_name=%s&vn_uuid=&mac=' % tor_name
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
                key_list = data.keys()
                val_pair = self.get_key_pair(data, key_list)
                all_snh_list.append(val_pair)
            elif type(value_list) == list:
                for data in value_list:
                    key_list = data.keys()
                    val_pair = self.get_key_pair(data, key_list)
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
                    key_list = data.keys()
                    val_pair = self.get_key_pair(data, key_list)
                    all_snh_list.append(val_pair)
                elif type(value_list) == list:
                    for data in value_list:
                        key_list = data.keys()
                        val_pair = self.get_key_pair(data, key_list)
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
                get_data = self.get_all_snh_dict(tdata[i], tkeys)
        all_snh_list = []

        for i in get_data:
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
        
    def get_key_pair(self, data, key_list):
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
                            pass
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
                                            pass
                                    elif type(idt[ik]) == dict:
                                        idt[ik] = self.get_data(idt[ik])
                                        idt[ik] = self.get_list(idt[ik])
                            dt_list.append(idt)
                        dt[k] = dt_list
            snh_list.append(dt)
        return snh_list
     
    def get_snh_dict_data(self,data):
        key = data.keys()
        if key[0].find('') == 0:
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
        data = data[key[0]]
        
        if type(data) == dict:
            data = self.get_nest_data(data)
            return data
        elif type(data) == list:
            all_data = []
            for idata in data:
                ndata = self.get_nest_data(idata)
                all_data = all_data + ndata
            return all_data
            
    def get_nest_data(self,data):
        rkeys = data.keys()
        try:
            rkeys.remove('more')
        except:
            pass
        data = self.get_data(data[rkeys[0]])
        if type(data[0]) != dict:
            return None
        data = self.get_snh_list(data)

        return data
    
    def get_data(self,data):
        while True:
            key = data.keys()
            if type(data[key[0]]) == str:
                break
            data = data[key[0]]
            if key[0].islower() == False:
                break
        data = self.get_all_snh_dict(data)
        return data
    
    def error_msg(self, oper, msg):
        msg = '\nFaild to get %s: %s\n' % (oper,msg)
        raise ValueError(msg)
