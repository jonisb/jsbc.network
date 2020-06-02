# -*- coding: utf-8 -*-
import unittest

import uuid
#from jsbc.network.ssdplib import REQUEST, REPLY, SSDP
from jsbc.network.ssdplib import REQUEST


class test_testing(unittest.TestCase):
    def test_REQUEST_no_data(self):
        request = REQUEST()
        assert request.id == None
        assert request.addr == None
        assert request.requestline == u'M-SEARCH * HTTP/1.1'
        #assert REQUEST() == {u'st': u'upnp:rootdevice', u'mx': u'3', u'man': u'"ssdp:discover"', u'host': u'239.255.255.250:1900'}
        assert bytes(request).splitlines()[0] == b'M-SEARCH * HTTP/1.1'
        assert {line.partition(b': ')[0]: line.partition(b': ')[2] for line in bytes(request).splitlines()[1:]} == {b'st': b'upnp:rootdevice', b'mx': b'3', b'man': b'"ssdp:discover"', b'host': b'239.255.255.250:1900', b'': b''}

    def test_REQUEST_with_data(self):
        request = REQUEST(bytes(REQUEST()))

        assert request.id == None
        assert request.addr == None
        assert request.requestline == u'M-SEARCH * HTTP/1.1'
        #assert request == {u'st': u'upnp:rootdevice', u'mx': u'3', u'man': u'"ssdp:discover"', u'host': u'239.255.255.250:1900'}, repr(request)
        assert bytes(request).splitlines()[0] == b'M-SEARCH * HTTP/1.1'
        assert {line.partition(b': ')[0]: line.partition(b': ')[2] for line in bytes(request).splitlines()[1:]} == {b'st': b'upnp:rootdevice', b'mx': b'3', b'man': b'"ssdp:discover"', b'host': b'239.255.255.250:1900', b'': b''}


    '''
    def test_REPLY_with_data(self):
        test_reply = b"""\
HTTP/1.1 200 OK\r
CACHE-CONTROL: max-age=120\r
ST: upnp:rootdevice\r
USN: uuid:e8d31334-41cd-4a9f-8950-bce16ff38738::upnp:rootdevice\r
EXT:\r
SERVER: ASUSTeK UPnP/1.0 MiniUPnPd/1.4\r
LOCATION: http://192.168.1.1:45701/rootDesc.xml\r
\r
"""
        reply = REPLY(test_reply, ('192.168.1.1', 1900))

        assert reply.statusline == u'HTTP/1.1 200 OK'
        assert reply.version == u'HTTP/1.1'
        assert reply.code == u'200'
        assert reply.codemsg == u'OK'

        assert reply.id == uuid.UUID('uuid:e8d31334-41cd-4a9f-8950-bce16ff38738'), reply.id
        assert reply.addr == ('192.168.1.1', 1900)
        assert reply[u'st'] == u'upnp:rootdevice', repr(reply[u'st'])
        assert reply[u'usn'] == u'uuid:e8d31334-41cd-4a9f-8950-bce16ff38738::upnp:rootdevice'
        assert reply[u'server'] == u'ASUSTeK UPnP/1.0 MiniUPnPd/1.4'
        assert reply[u'location'] == u'http://192.168.1.1:45701/rootDesc.xml'
        assert reply[u'cache-control'] == u'max-age=120'
        assert reply[u'ext'] == u'', repr(reply[u'ext'])
        #assert reply == {u'st': u'upnp:rootdevice', u'usn': u'uuid:e8d31334-41cd-4a9f-8950-bce16ff38738::upnp:rootdevice', u'server': u'ASUSTeK UPnP/1.0 MiniUPnPd/1.4', u'location': u'http://192.168.1.1:45701/rootDesc.xml', u'cache-control': u'max-age=120', u'ext': u''}, repr(reply)
        #assert bytes(reply).splitlines()[0] == b'HTTP/1.1 200 OK', bytes(reply)
        #assert {line.partition(b': ')[0]: line.partition(b': ')[2] for line in bytes(reply).splitlines()[1:]} == {b'st': b'upnp:rootdevice', b'usn': b'uuid:e8d31334-41cd-4a9f-8950-bce16ff38738::upnp:rootdevice', b'server': b'ASUSTeK UPnP/1.0 MiniUPnPd/1.4', b'location': b'http://192.168.1.1:45701/rootDesc.xml', b'cache-control': b'max-age=120', b'ext': b'', b'': b''}

    '''
    #def test_ssdplibclass(self):
    #    ssdp = SSDP()

    #    handleRequestQueue()
