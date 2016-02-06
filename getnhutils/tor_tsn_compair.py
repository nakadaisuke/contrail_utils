import argparse
import sys
import copy
from ovsdb_schema_reader import *
from contrail_sandeshlibs import *

class CompareOvsdbTsn(object):
    def __init__(self,tsn_list):
        tor_ip_port = self.get_active_tor(tsn_list)
        self.tsn = GetContrailSandesh(hostname=tor_ip_port[0],port=tor_ip_port[1])
    
    def get_ovsdb_dump(self,hostname='',port=''):
        tor = GetOvsdbColumns(hostname=hostname,port=int(port))
        try:
            tor.open_socket()
            ovsdb_dump = tor.get_ovsdb_dump()
            tor.close_socket()
            return ovsdb_dump
        except:
            msg = 'KeyError: Could not get ovsdb dump %s:%s' % (hostname,port)
            raise
    
    def get_active_tor(self,tsn_list):
        for i in tsn_list:
            tor_ip_port = i.split(':')
            tsn = GetContrailSandesh(hostname=tor_ip_port[0],port=tor_ip_port[1])
            ovsdb_pswitch = tsn.get_ovsdb_physical_switch()
            if type(ovsdb_pswitch['OvsdbPhysicalSwitchResp']['pswitch']) == dict:
                return tor_ip_port
        msg = 'KeyError: Could not get active TSN'
        print msg
        raise 
    
    def get_tsn_ovsdb_dump(self,tor_conn):
        tor_conn_data = tor_conn.split(':')
        dump_data = self.get_ovsdb_dump(hostname=tor_conn_data[0],port=int(tor_conn_data[1]))
        tor_name = dump_data['Physical_Switch']['result'][0]['rows'][0]['name']
        if self.chk_tor_name(tor_name) == False:
            msg = 'KeyError: Could not match ToR name %s' % tor_name
            print msg
            raise
    
        tsn_key_list={'tsn_client':'get_ovsdb_client','tsn_psw':'get_ovsdb_physical_switch','tsn_pport':'get_ovsdb_physical_port','tsn_lsw':'get_ovsdb_logical_switch','tsn_vport':'get_ovsdb_vlan_port_binding','tsn_uc_mac_local':'get_ovsdb_unicast_mac_local','tsn_vrf':'get_ovsdb_vrf','tsn_mc_mac_local':'get_ovsdb_multicast_mac_local'}
        ovsdb_key_list=['Logical_Switch','Mcast_Macs_Local','Mcast_Macs_Remote','Physical_Locator','Physical_Locator_Set','Physical_Port','Physical_Switch','Tunnel','Ucast_Macs_Local','Ucast_Macs_Remote']
    
        tsn_table = self.get_tsn_table(tsn_key_list)
        ovsdb_table = self.get_ovsdb_table(dump_data,ovsdb_key_list)
    
        return tsn_table,ovsdb_table
    
    def get_ovsdb_table(self,dump_data,ovsdb_key_list):
        ovsdb_table_list = {}
        for key in ovsdb_key_list:
            data = dump_data[key]['result'][0]['rows']
            ovsdb_table_list[key] = data
        return ovsdb_table_list
    
    def get_tsn_table(self,tsn_key_list):
        tsn_table_list = {}
        for k in tsn_key_list:
            exe_txt = 'data = self.tsn.%s()' % (tsn_key_list[k])
            exec(exe_txt)
            tsn_table_list[k] = data
        return tsn_table_list
    
    def get_lsw_uuid(self,ovsdb_table,logical_switch):
        lsw_uuid = None
        for i in ovsdb_table['Logical_Switch']:
            if i['_uuid'][1] == logical_switch:
                lsw_uuid = i['name'].replace('Contrail-','')
        return lsw_uuid
    
    def get_locator_dst_ip(self,ovsdb_table,locator_set):
        for i in ovsdb_table['Physical_Locator']:
            if i['_uuid'][1] == locator_set:
                locator_dst_ip = i['dst_ip']
                return locator_dst_ip
        return None
    
    def get_locator_set_dst_ip(self,ovsdb_table,locator_set):
        locator_uuid = None
        for i in ovsdb_table['Physical_Locator_Set']:
            if i['_uuid'][1] == locator_set:
                locator_uuid = i['locators'][1]
            if locator_uuid != None:
                for i in ovsdb_table['Physical_Locator']:
                    if i['_uuid'][1] == locator_uuid:
                        locator_dst_ip = i['dst_ip']
                        return locator_dst_ip
        return None
    
    def compair_tables(self,tsn_tables,ovsdb_tables):
        data_list = []
        for i in tsn_tables:
            flag = True
            tsn_data = copy.copy(i)
            del tsn_data[0]
            if tsn_data not in ovsdb_tables:
                flag = 'NotInOVSDB'
            else:
                ovsdb_tables.remove(tsn_data)
            if i[0] != 'In sync(4)':
                flag = 'NotSync'
            flag = {'flag':flag}
            data = [flag, i]
            data_list.append(data)
        if len(ovsdb_tables) != 0:
            for i in ovsdb_tables:
                flag = {'flag':'NotInTSN'}
                data = [flag, i]
                data_list.append(data)
        return data_list

    def chk_tor_name(self,tor_name):
        ovsdb_pswitch = self.tsn.get_ovsdb_physical_switch()
        if type(ovsdb_pswitch['OvsdbPhysicalSwitchResp']['pswitch']) == list:
            tsn_tor_name = ovsdb_pswitch['OvsdbPhysicalSwitchResp']['pswitch'][0]['name']
            if tor_name == tsn_tor_name:
                return True
            else:
                return False
    
    def chk_physical_switch(self,tsn_table,ovsdb_table):
        tsn_table = tsn_table['tsn_psw']['OvsdbPhysicalSwitchResp']['pswitch']
        tsn_state = tsn_table['state']
        tsn_name = tsn_table['name']
        tsn_tunnel_ip = tsn_table['tunnel_ip']
        
        ovsdb_name = ovsdb_table['Physical_Switch'][0]['name']
        ovsdb_tunnel_ip = ovsdb_table['Physical_Switch'][0]['tunnel_ips']
        
        flag = {'flag':True}
        if tsn_state != 'In sync(4)':
            flag = {'flag':'NotSync'} 
        if tsn_name != ovsdb_name:
            flag = {'flag':'InvalidName'}
        if tsn_tunnel_ip != ovsdb_tunnel_ip:
            flag = {'flag':'InvalidTunnelIP'}
        pw_data = [tsn_state,tsn_name,tsn_tunnel_ip]
        return [[flag, pw_data]]
    
    def chk_logical_switch(self,tsn_table,ovsdb_table):
        tsn_table = tsn_table['tsn_lsw']['OvsdbLogicalSwitchResp']['lswitch']
        tsn_lsw_list = []
        for i in tsn_table:
            lsw_list = [i['state'],i['name'],i['vxlan_id']]
            tsn_lsw_list.append(lsw_list)
        ovsdb_lsw_list = []
        for i in ovsdb_table['Logical_Switch']:
            ovsdb_name = i['name'].replace('Contrail-','')
            lsw_list = [ovsdb_name,str(i['tunnel_key'])]
            ovsdb_lsw_list.append(lsw_list)
        chk_list = self.compair_tables(tsn_lsw_list,ovsdb_lsw_list)
        return chk_list
    
    def chk_mcast_macs_local(self,tsn_table,ovsdb_table):
        tor_tunnel_ip = tsn_table['tsn_psw']['OvsdbPhysicalSwitchResp']['pswitch']['tunnel_ip']
        tsn_table = tsn_table['tsn_mc_mac_local']['OvsdbMulticastMacLocalResp']['macs']
        tsn_mc_mac_list = []
        for i in tsn_table:
            mc_mac_list = [i['state'],i['mac'],i['logical_switch'],tor_tunnel_ip]
            tsn_mc_mac_list.append(mc_mac_list)
        ovsdb_mc_mac_list = []
        for i in ovsdb_table['Mcast_Macs_Local']:
            logical_switch = self.get_lsw_uuid(ovsdb_table,i['logical_switch'][1])
            locator_set = self.get_locator_set_dst_ip(ovsdb_table,i['locator_set'][1])
            if i['MAC'] == 'unknown-dst':
                mac = 'ff:ff:ff:ff:ff:ff'
            else:
                mac = i['MAC']
            mc_mac_list = [mac,logical_switch,locator_set]
            ovsdb_mc_mac_list.append(mc_mac_list)
        chk_list = self.compair_tables(tsn_mc_mac_list,ovsdb_mc_mac_list)
        return chk_list
    
    def chk_mcast_macs_remote(self,tsn_table,ovsdb_table):
        lswitch_table = tsn_table['tsn_lsw']['OvsdbLogicalSwitchResp']['lswitch']
        tor_ip = tsn_table['tsn_client']['OvsdbClientResp']['client']['tor_service_node']
        tsn_table = tsn_table['tsn_mc_mac_local']['OvsdbMulticastMacLocalResp']['macs']
        tsn_mc_mac_list = []
        for i in tsn_table:
            mc_mac_list = [i['state'],i['mac'],i['logical_switch'],tor_ip]
            tsn_mc_mac_list.append(mc_mac_list)
        ovsdb_mc_mac_list = []
        for i in ovsdb_table['Mcast_Macs_Remote']:
            logical_switch = self.get_lsw_uuid(ovsdb_table,i['logical_switch'][1])
            locator_set = self.get_locator_set_dst_ip(ovsdb_table,i['locator_set'][1])
            if i['MAC'] == 'unknown-dst':
                mac = 'ff:ff:ff:ff:ff:ff'
            else:
                mac = i['MAC']
            mc_mac_list = [mac,logical_switch,locator_set]
            ovsdb_mc_mac_list.append(mc_mac_list)
        chk_list = self.compair_tables(tsn_mc_mac_list,ovsdb_mc_mac_list)
        return chk_list
    
    def chk_physical_port(self,tsn_table,ovsdb_table):
        tsn_table = tsn_table['tsn_pport']['OvsdbPhysicalPortResp']['port']
        tsn_pport_list = []
        for i in tsn_table:
            vlan_list = []
            if i['vlans'] != '':
                if type(i['vlans']) == list:
                    for j in i['vlans']:
                        vlan = [j['vlan'],j['logical_switch']]
                        vlan_list.append(vlan)
                elif type(i['vlans']) == dict:
                    vlan = [i['vlans']['vlan'],i['vlans']['logical_switch']]
                    vlan_list.append(vlan)
            pport_list = [i['state'],vlan_list,i['name']]
            tsn_pport_list.append(pport_list)
        
        ovsdb_pport_list = []
        for i in ovsdb_table['Physical_Port']:
            vlan_list = []
            if len(i['vlan_bindings'][1]) != 0:
                for j in i['vlan_bindings'][1]:
                    lsw_uuid = self.get_lsw_uuid(ovsdb_table,j[1][1])
                    vlan = [str(j[0]),lsw_uuid]
                    vlan_list.append(vlan)
            pport_list = [vlan_list,i['name']]
            ovsdb_pport_list.append(pport_list)
        chk_list = self.compair_tables(tsn_pport_list,ovsdb_pport_list)
        return chk_list
    
    def chk_ucast_macs_local(self,tsn_table,ovsdb_table):
        tsn_table = tsn_table['tsn_uc_mac_local']['OvsdbUnicastMacLocalResp']['macs']
        tsn_uc_local_mac_list = []
        for i in tsn_table:
            uc_local_mac_list = [i['state'],i['mac'],i['logical_switch'],i['dest_ip']]
            tsn_uc_local_mac_list.append(uc_local_mac_list)
    
        ovsdb_uc_local_mac_list = []
        for i in ovsdb_table['Ucast_Macs_Local']:
            logical_switch = self.get_lsw_uuid(ovsdb_table,i['logical_switch'][1])
            dst_ip = self.get_locator_dst_ip(ovsdb_table,i['locator'][1])
            uc_local_mac_list = [i['MAC'],logical_switch,dst_ip]
            ovsdb_uc_local_mac_list.append(uc_local_mac_list)
        chk_list = self.compair_tables(tsn_uc_local_mac_list,ovsdb_uc_local_mac_list)
        return chk_list
    
    def chk_ucast_macs_remote(self,tsn_table,ovsdb_table):
        remote_macs_list = []
        for i in tsn_table['tsn_lsw']['OvsdbLogicalSwitchResp']['lswitch']:
            lsw_uuid = i['name']
            remote_macs = self.tsn.get_ovsdb_unicast_mac_remote(logical_switch=lsw_uuid)
            remote_macs = remote_macs['OvsdbUnicastMacRemoteResp']['macs']
            if len(remote_macs) != 0:
                for j in remote_macs:
                    if j['dest_ip'] != 0 and j['self_exported'] == 'false':
                        remote_macs_list.append(j)
        
        tsn_uc_remote_mac_list = []
        for i in remote_macs_list:
            uc_remote_mac_list = [i['state'],i['mac'],i['logical_switch'],i['dest_ip']]
            tsn_uc_remote_mac_list.append(uc_remote_mac_list)
        
        ovsdb_uc_remote_mac_list = []
        for i in ovsdb_table['Ucast_Macs_Remote']:
            logical_switch = self.get_lsw_uuid(ovsdb_table,i['logical_switch'][1])
            dst_ip = self.get_locator_dst_ip(ovsdb_table,i['locator'][1])
            uc_remote_mac_list = [i['MAC'],logical_switch,dst_ip]
            ovsdb_uc_remote_mac_list.append(uc_remote_mac_list)
        chk_list = self.compair_tables(tsn_uc_remote_mac_list,ovsdb_uc_remote_mac_list)
        return chk_list
