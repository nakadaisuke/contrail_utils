import sys
import xmldict
import urllib2
from xml.etree.ElementTree import *

class GetSandeshVrouter(object):
    def __init__(self, hostname='127.0.0.1', port='8085', *args, **karwgs):
        self.hostname = hostname
        self.port = str(port)


    def snhdict(self, path):
        url = 'http://%s:%s/%s' % (self.hostname, self.port, path)
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req)
            xmldata = response.read()
        except:
            self._error_msg('get_xml', url)
            raise

        xml_dict = xmldict.xml_to_dict(xmldata)
        return xml_dict


    def get_vxlan(self, vni):
        path = 'Snh_KVxLanReq?vxlan_label=%s' % str(vni)
        vxlan_dict = self.snhdict(path)
        if vxlan_dict.has_key('ErrResp')  == True:
            self._error_msg('vxlan', vni)
            raise
        else:
            return vxlan_dict


    def get_nh(self, nhid):
        path = 'Snh_KNHReq?x=%s' % str(nhid)
        nh_dict = self.snhdict(path)
        if nh_dict.has_key('InternalErrResp') == True:
            self._error_msg('get_nh', nhid)
            raise
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
            self._error_msg('get_l2route', vrfid)
            raise


    def get_itf(self):
        path = 'Snh_PageReq?x=begin:-1,end:-1,table:db.interface.0,'
        try:
            itf_dict = self.snhdict(path)
            return itf_dict
        except:
            self._error_msg('get_itf', self.hostname)
            raise


    def get_mcast_comp(self, vni):
        vxlan_dict = self.get_vxlan(vni)
        try:
            nhid = vxlan_dict['KVxLanResp']['vxlan_list']['list']['KVxLanInfo']['nhid']['#text']
        except:
            self._error_msg('vxlan_dict', vni)
            raise

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
           self._error_msg('get_mcast_tree', vni)
           raise


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
            self._get_tunnel(i, tunnel_list)

        return tunnel_list, tap_list


    def _get_tunnel(self, mc_index, tunnel_list):
        nh_data = self.get_nh(mc_index)
        if nh_data['KNHResp']['nh_list']['list']['KNHInfo']['type']['#text'] == 'COMPOSITE':
            try:
                if type(nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']) == list:
                    for i in nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']:
                        self._get_tunnel(i['nh_id']['#text'], tunnel_list)
                else:
                    i = nh_data['KNHResp']['nh_list']['list']['KNHInfo']['component_nh']['list']['KComponentNH']['nh_id']['#text']
                    self._get_tunnel(i, tunnel_list)
            except:
                pass
        elif nh_data['KNHResp']['nh_list']['list']['KNHInfo']['type']['#text'] == 'TUNNEL':
            tunnel_list.append(nh_data)

        return tunnel_list
    
    

    def _error_msg(self, oper, msg):
        msg = '\nFaild to get %s: %s\n' % (oper,msg)
        print msg
        
