import sys
import xmldict
import urllib2
from xml.etree.ElementTree import *

class GetContrailSandesh(object):
    def __init__(self, hostname='127.0.0.1', port='8085'):
        self.hostname = hostname
        self.port = str(port)

    def snhdict(self, path):
        url = 'http://%s:%s/%s' % (self.hostname, self.port, path)
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
            xmldata = response.read()
        except:
            self.__error_msg__('get_xml', url)

        xml_dict = xmldict.xml_to_dict(xmldata)
        return xml_dict

    def get_sg_list(self):
        #Return SgListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.sg.0,'
        rsp = self.snhdict(path)
        root_dict = rsp['__SgListResp_list']['SgListResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_vn_list(self):
        #Return VnListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vn.0,'
        rsp = self.snhdict(path)
        root_dict = rsp['__VnListResp_list']['VnListResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_vm_list(self):
        #Return VmListResp by dict
        #['uuid'] 
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vm.0,'
        rsp = self.snhdict(path)
        root_dict = rsp['__VmListResp_list']['VmListResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_nh_list(self):
        #Return NhListResp by dict
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.nexthop.0,'
        rsp = self.snhdict(path)
        root_dict = rsp['__NhListResp_list']['NhListResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_vrf_list(self):
        #Return VrfListResp by dict
        keys = ['vrf_list','list','VrfSandeshData']
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.vrf.0,'
        rsp = self.snhdict(path)
        root_dict = rsp['__VrfListResp_list']['VrfListResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_inet4_uc_route(self, vrf_index):
        #Return Inet4UcRouteResp by dict
        path = 'Snh_Inet4UcRouteReq?vrf_index=%s&src_ip=&prefix_len=&stale=' % vrf_index
        path = self.__get_data_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__Inet4UcRouteResp_list']['Inet4UcRouteResp']
        all_snh_list = self.__get_all_snh__(root_dict)
        return all_snh_list

    def get_vxlan(self, vni):
        path = 'Snh_KVxLanReq?vxlan_label=%s' % str(vni)
        vxlan_dict = self.snhdict(path)
        if vxlan_dict.has_key('ErrResp')  == True:
            self.__error_msg__('vxlan', vni)
        else:
            return vxlan_dict

    def get_nh(self, nhid):
        path = 'Snh_KNHReq?x=%s' % str(nhid)
        nh_dict = self.snhdict(path)
        if nh_dict.has_key('InternalErrResp') == True:
            self.__error_msg__('get_nh', nhid)
        else:
            return nh_dict

    def get_l2route(self, vrfid):
        path = 'Snh_Layer2RouteReq?x=%s' % str(vrfid)
        try:
            l2route_dict = self.snhdict(path)
            all_path = l2route_dict['__Layer2RouteResp_list']['Pagination']['req']['PageReqData']['all']['#text']
            all_path = 'Snh_PageReq?x=%s' % all_path
            all_l2route_dict = self.snhdict(all_path)
            return all_l2route_dict
        except:
            self.__error_msg__('get_l2route', vrfid)

    def get_itf(self):
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.interface.0,'
        try:
            itf_dict = self.snhdict(path)
            return itf_dict
        except:
            self.__error_msg__('get_itf', self.hostname)

    def get_mcast_comp(self, vni):
        vxlan_dict = self.get_vxlan(vni)
        try:
            nhid = vxlan_dict['KVxLanResp']['vxlan_list']['list']['KVxLanInfo']['nhid']['#text']
        except:
            self.__error_msg__('vxlan_dict', vni)

        nh_dict = self.get_nh(nhid)
        vrfid = nh_dict['KNHResp']['nh_list']['list']['KNHInfo']['vrf']['#text']
        
        l2route_dict = self.get_l2route(vrfid)
        if type(l2route_dict['__BridgeRouteResp_list']['BridgeRouteResp']) == list:
            for i in l2route_dict['__BridgeRouteResp_list']['BridgeRouteResp']:
                 if type(i['route_list']['list']['RouteL2SandeshData']) == list:
                     for h in i['route_list']['list']['RouteL2SandeshData']:
                         if h['mac']['#text'] == 'ff:ff:ff:ff:ff:ff':
                             mcast_d = h['path_list']
                 else:
                     h = i['route_list']['list']['RouteL2SandeshData']['route_list']['list']['RouteL2SandeshData']
                     if h['mac']['#text'] == 'ff:ff:ff:ff:ff:ff':
                         mcast_d = h['path_list']
            
            for i in mcast_d['list']['PathSandeshData']:
                if i['peer']['#text'] == 'Multicast':
                     mcast_tree =  i
                     return mcast_tree

        elif type(l2route_dict['__BridgeRouteResp_list']['BridgeRouteResp']) == dict:
            for i in l2route_dict['__BridgeRouteResp_list']['BridgeRouteResp']['route_list']['list']['RouteL2SandeshData']:
                if i['mac']['#text'] == 'ff:ff:ff:ff:ff:ff':
                     mcast_d = i['path_list']
                
            for i in mcast_d['list']['PathSandeshData']:
                if i['peer']['#text'] == 'Multicast':
                     mcast_tree =  i
                     return mcast_tree
        else:
           self.__error_msg__('get_mcast_tree', vni)

    def get_nh_data(self, vni):
        tap_list = []
        tunnel_list = []
        nh_index_list = []
        mcast_comp_data = self.get_mcast_comp(vni)
        if type(mcast_comp_data['nh']['NhSandeshData']['mc_list']['list']['McastData']) == list:
            for i in mcast_comp_data['nh']['NhSandeshData']['mc_list']['list']['McastData']:
                if i['type']['#text'] == 'Interface':
                    tap_list.append(i)
        else:
            i = mcast_comp_data['nh']['NhSandeshData']['mc_list']['list']['McastData']
            if i['type']['#text'] == 'Interface':
                tap_list.append(i)

        mc_index = mcast_comp_data['nh']['NhSandeshData']['nh_index']['#text']
        mc_list = self.get_nh(mc_index)['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']
        if type(mc_list) == list:
            for i in mc_list:
                nh_index_list.append(i['nh_id']['#text'])
        else:
            nh_index_list.append(mc_list['nh_id']['#text'])

        for i in nh_index_list:
            self.__get_tunnel__(i, tunnel_list)

        return tunnel_list, tap_list

    def __get_tunnel__(self, mc_index, tunnel_list):
        nh_data = self.get_nh(mc_index)
        if nh_data['KNHResp']['nh_list']['list']['KNHInfo']['type']['#text'] == 'COMPOSITE':
            try:
                if type(nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']) == list:
                    for i in nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']:
                        self.__get_tunnel__(i['nh_id']['#text'], tunnel_list)
                else:
                    i = nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']['nh_id']['#text']
                    self.__get_tunnel__(i, tunnel_list)
            except:
                pass
        elif nh_data['KNHResp']['nh_list']['list']['KNHInfo']['type']['#text'] == 'TUNNEL':
            tunnel_list.append(nh_data)

        return tunnel_list

    def get_ovsdb_client(self):
        #Return OvsdbClientResp by list 
        #['status', 'remote_ip', 'remote_port', 'connection_time'['txn_initiated', 'txn_succeeded', 'txn_failed', 'txn_pending', 'pending_send_msg']]
        key_list = ['status', 'remote_ip', 'remote_port', 'connection_time']
        txn_key_list = ['txn_initiated', 'txn_succeeded', 'txn_failed', 'txn_pending', 'pending_send_msg']
        path = 'Snh_OvsdbClientReq'
        try:
            rsp = self.snhdict(path)
            data = rsp['OvsdbClientResp']['client']['SandeshOvsdbClient']['sessions']['list']['SandeshOvsdbClientSession'] 
            tor_status = self.__get_key_value__(data, key_list)
            data = data['txn_stats']['SandeshOvsdbTxnStats']
            txn_status = self.__get_key_value__(data, txn_key_list) 
            tor_status.append(txn_status)
            return tor_status
        except:
            return 'tor switch is not found' 

    def get_physical_switch(self):
        #Return OvsdbPhysicalSwitchResp by list
        #['state', 'name', 'tunnel_ip'] 
        key_list = ['state', 'name', 'tunnel_ip']
        path = 'Snh_OvsdbPhysicalSwitchReq?session_remote_ip=&session_remote_port='
        try:
            rsp = self.snhdict(path)
            data = rsp['OvsdbPhysicalSwitchResp']['pswitch']['list']['OvsdbPhysicalSwitchEntry']
            tor_data = self.__get_key_value__(data, key_list) 
            return tor_data
        except:
            self.__error_msg__('get_physical_switch', 'no valid value')

    def get_physical_port(self):
        #Return OvsdbPhysicalSwitchResp by list
        #['state', 'switch_name', 'name'['vlan', 'logical_switch', 'in_pkts', 'in_bytes', 'out_pkts', 'out_bytes']]
        #if VLAN is not attached to the interface, return None
        keys = ['port','list','OvsdbPhysicalPortEntry']
        key_list = ['state', 'switch_name', 'name', 'vlans']
        vlan_key_list = ['vlan', 'logical_switch', 'in_pkts', 'in_bytes', 'out_pkts', 'out_bytes']
        path = 'Snh_OvsdbPhysicalPortReq?session_remote_ip=&session_remote_port=&name='
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbPhysicalPortResp_list']['OvsdbPhysicalPortResp'] 
        all_pp_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        all_snh_list = []
        for pp_list in all_pp_list:
            if pp_list[3]['list'].has_key('OvsdbPhysicalPortVlanInfo'):
                val = self.__get_all_snh_list__(pp_list[3],['list','OvsdbPhysicalPortVlanInfo'],vlan_key_list)
                pp_list[3] = val
            else:
                pp_list[3] = None
            all_snh_list.append(pp_list)
        return all_snh_list

    def get_logical_switch(self):
        #Return OvsdbLogicalSwitchResp by list
        #['state', 'name', 'physical_switch', 'vxlan_id', 'tor_service_node']
        keys = ['lswitch','list','OvsdbLogicalSwitchEntry']
        key_list = ['state', 'name', 'physical_switch', 'vxlan_id', 'tor_service_node']
        path = 'Snh_OvsdbLogicalSwitchReq?session_remote_ip=&session_remote_port=&name='
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbLogicalSwitchResp_list']['OvsdbLogicalSwitchResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        return all_snh_list

    def get_vlan_port_binding(self):
        #Return OvsdbVlanPortBindingResp by list
        #['state', 'physical_port', 'physical_device', 'logical_switch', 'vlan']
        keys = ['bindings','list','OvsdbVlanPortBindingEntry']
        key_list = ['state', 'physical_port', 'physical_device', 'logical_switch', 'vlan']
        path = 'Snh_OvsdbVlanPortBindingReq?session_remote_ip=&session_remote_port=&physical_port='
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbVlanPortBindingResp_list']['OvsdbVlanPortBindingResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list) 
        return all_snh_list

    def get_ucast_mac_local(self):
        #Return OvsdbUnicastMacLocalResp by list
        #['state', 'mac', 'logical_switch', 'dest_ip']
        keys = ['macs','list','OvsdbUnicastMacLocalEntry']
        key_list = ['state', 'mac', 'logical_switch', 'dest_ip']
        path = 'Snh_OvsdbUnicastMacLocalReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        path = self.__get_ovsdb_page__(path)
        if path == False:
            return 'no unicast mac local'
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbUnicastMacLocalResp_list']['OvsdbUnicastMacLocalResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        return all_snh_list

    def get_vrf(self):
        #Return OvsdbVrfResp by list
        #['state', 'logical_switch', 'unicast_remote_table']
        keys = ['vrfs','list','OvsdbVrfEntry']
        key_list = ['state', 'logical_switch', 'unicast_remote_table']
        path = 'Snh_OvsdbVrfReq?session_remote_ip=&session_remote_port=&logical_switch=&mac='
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbVrfResp_list']['OvsdbVrfResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        return all_snh_list

    def get_ucast_mac_remote(self, ls_uuid):
        #Return OvsdbUnicastMacRemoteResp by list
        #['state', 'mac', 'logical_switch','dest_ip' ,'self_exported' ,'sequence', 'self_sequence', 'ecmp_suppressed']
        keys = ['macs','list','OvsdbUnicastMacRemoteEntry']
        key_list = ['state','mac','logical_switch','dest_ip','self_exported','sequence','self_sequence','ecmp_suppressed']
        path = 'Snh_OvsdbUnicastMacRemoteReq?session_remote_ip=&session_remote_port=&logical_switch=%s&mac=' % ls_uuid
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbUnicastMacRemoteResp_list']['OvsdbUnicastMacRemoteResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        return all_snh_list

    def get_mcast_mac_local(self):
        #Return OvsdbMulticastMacLocalResp by list
        #['state', 'mac' , 'logical_switch', 'vxlan_id']
        keys = ['macs', 'list', 'OvsdbMulticastMacLocalEntry']
        key_list = ['state', 'mac' , 'logical_switch', 'vxlan_id']
        path = 'Snh_OvsdbMulticastMacLocalReq?session_remote_ip=&session_remote_port=&logical_switch='
        path = self.__get_ovsdb_page__(path)
        rsp = self.snhdict(path)
        root_dict = rsp['__OvsdbMulticastMacLocalResp_list']['OvsdbMulticastMacLocalResp']
        all_snh_list = self.__get_all_snh_list__(root_dict, keys, key_list)
        return all_snh_list 

    def get_all_ucast_mac_remote(self):
        #Return all of OvsdbUnicastMacRemoteReq by Dict which key is vrf-uuid
        vrf_list = []
        all_snh_data = {}
        vrf_data = self.get_vrf()
        for vrf in vrf_data:
            vrf_list.append(vrf[1])

        for vrf in vrf_list:
            umr_data = self.get_ucast_mac_remote(vrf)
            all_snh_data[vrf] = umr_data 
        
        return all_snh_data

    def __get_data_page__(self, path):
        try:
            rsp = self.snhdict(path)
            top_key = rsp.keys()
            url = rsp[top_key[0]]['Pagination']['req']['PageReqData']['all']['#text']
            all_path = 'Snh_PageReq?x=%s' % (url)
            return all_path
        except:
            return False

    def __get_ovsdb_page__(self, path):
        try:
            rsp = self.snhdict(path)
            top_key = rsp.keys()
            url = rsp[top_key[0]]['OvsdbPageResp']['req']['OvsdbPageRespData']['all']['#text']
            all_path = 'Snh_OvsdbPageReq?x=%s' % (url)
            return all_path
        except:
            return False

    def __get_all_snh_list__(self, root_dict, keys, key_list):
        all_snh_list = []
        if type(root_dict) == dict:
            value_list = root_dict
            for key in keys:
                value_list = value_list[key]
            if type(value_list) == dict:
                data = value_list
                val_pair = self.__get_key_value__(data, key_list)
                all_snh_list.append(val_pair)
            elif type(value_list) == list:
                for data in value_list:
                    val_pair = self.__get_key_value__(data, key_list)
                    all_snh_list.append(val_pair)

        elif type(root_dict) == list:
            for page in root_dict:
                value_list = page
                for key in keys:
                    value_list = value_list[key]
                if type(value_list) == dict:
                    data = value_list
                    val_pair = self.__get_key_value__(data, key_list)
                    all_snh_list.append(val_pair)
                elif type(value_list) == list:
                    for data in value_list:
                        val_pair = self.__get_key_value__(data, key_list)
                        all_snh_list.append(val_pair)

        else:
            self.__error_msg__('get_all_snh_list','no valid list')

        return all_snh_list

    def __get_key_value__(self, data, key_list):
                data_pair = []
                for key in key_list:
                   try:
                       data_pair.append(data[key]['#text']) 
                   except:
                       if data[key].has_key('list'):
                           data_pair.append(data[key])
                       else:
                           data_pair.append(None)
                return data_pair

    def __get_all_snh_dict__(self, root_dict, keys=None):
        all_snh_list = []
        if type(root_dict) == dict:
            value_list = root_dict
            if keys != None:
                for key in keys:
                    value_list = value_list[key]
            if type(value_list) == dict:
                data = value_list
                key_list = data.keys()
                val_pair = self.__get_key_pair__(data, key_list)
                all_snh_list.append(val_pair)
            elif type(value_list) == list:
                for data in value_list:
                    key_list = data.keys()
                    val_pair = self.__get_key_pair__(data, key_list)
                    all_snh_list.append(val_pair)

        elif type(root_dict) == list:
            for page in root_dict:
                value_list = page
                for key in keys:
                    value_list = value_list[key]
                if type(value_list) == dict:
                    data = value_list
                    key_list = data.keys()
                    val_pair = self.__get_key_pair__(data, key_list)
                    all_snh_list.append(val_pair)
                elif type(value_list) == list:
                    for data in value_list:
                        key_list = data.keys()
                        val_pair = self.__get_key_pair__(data, key_list)
                        all_snh_list.append(val_pair)

        else:
            self.__error_msg__('get_all_snh_list','no valid list')

        return all_snh_list

    def __get_all_snh__(self, root_dict):
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
                get_data = self.__get_all_snh_dict__(tdata[i], tkeys)
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
                    tdata[i] = self.__get_all_snh_dict__(tdata[i], tkeys)
                    all_snh_list.append(tdata)
                else:
                    all_snh_list.append(tdata)
        
        return all_snh_list
        
    def __get_key_pair__(self, data, key_list):
                data_pair = {}
                for key in key_list:
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

    def __error_msg__(self, oper, msg):
        msg = '\nFaild to get %s: %s\n' % (oper,msg)
        raise ValueError(msg)
