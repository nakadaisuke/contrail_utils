import socket
import json


class GetOvsdbColumns(object):

    def __init__(self, hostname="127.0.0.1", port=9999, *args, **karwgs):
        self.hostname = hostname
        self.port = port
        self.buffer_size = 2**12
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def open_socket(self):
        try:
            self.socket.connect((self.hostname, self.port))
        except socket.error, e:
            errcode = e[0]
            if errcode == 106:
                print "Connection already available"
                pass
            if errcode == 111:
                print "Connection refused %s:%s" % (self.hostname, self.port)

    def close_socket(self):
        self.socket.close()

    def get_json(self, columns_list):
        response = ''
        msg = ''
        lc = rc = 0
        self.socket.sendall(json.dumps(columns_list))
        while True:
            response = self.socket.recv(self.buffer_size)
            msg = msg + response
            for c in response:
                if c == '{':
                    lc += 1
                elif c == '}':
                    rc += 1

                if lc == rc and lc is not 0:
                    msg = json.loads(msg)
                    return msg

    def get_ovsdb_table(self):
        json_msg = {'method': 'get_schema',
                    'params': ['hardware_vtep'], 'id': 0}
        row_data = self.get_json(json_msg)
        row_table = row_data['result']['tables']
        table_list = row_table.keys()
        return table_list

    def get_table_schema(self, table):
        param = ['hardware_vtep', {
            'op': 'select', 'table': table, 'where': []}]
        json_msg = {'method': 'transact', 'id': 0, 'params': param}
        json_data = self.get_json(json_msg)
        return json_data

    def get_ovsdb_dump(self):
        schema_list = {}
        table_list = self.get_ovsdb_table()
        for table in table_list:
            schema = self.get_table_schema(table)
            schema_list[table] = schema
        return schema_list
