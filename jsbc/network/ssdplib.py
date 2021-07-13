# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import uuid
import collections
import logging

logger = logging.getLogger(__name__)

address = collections.namedtuple('address', ['host', 'port'])
ssdpaddr = address('239.255.255.250', 1900)


class BASE():
    def __str__(self):
        try:
            headers = [self.requestline]
        except AttributeError:
            headers = [self.statusline]

        #for header in self:
        #    headers.append(f"{header}: {self[header]}")
        for header in self.headers:
            #headers.append(f"{header}: {self.headers[header]}")
            headers.append("{0}: {1}".format(header, self.headers[header]))
        return "\r\n".join(headers + ['\r\n'])

    def __repr__(self):
        #return f"{self.addr}\n{self}"
        return "{0}\n{1}".format(self.addr, self)

    def __bytes__(self):
        return self.__str__().encode('latin-1')


def getheaders(headers):
    try:
        import http.client
        import io
    except ImportError:
        from mimetools import Message
        from StringIO import StringIO

        return Message(StringIO(headers))

    class _FakeSocket(io.BytesIO):
        def makefile(self, *args, **kw):
            return self

    return http.client.parse_headers(_FakeSocket(headers))


class REQUEST(BASE):
    def __init__(self, message=None, addr=None, method='M-SEARCH', path='*', version='HTTP/1.1'):
        if message is not None:
            message = message.rstrip().splitlines()
            self.requestline = message[0].decode('latin-1')
            self.method, self.path, self.version = self.requestline.split()
            if self.method in ('M-SEARCH', 'NOTIFY'):
                headers = b"\r\n".join(message[1:])
                self.headers = getheaders(headers)
                try:
                    self.id = uuid.UUID(self.headers['USN'].split('::')[0])
                except (AttributeError, KeyError):
                    self.id = None
            else:
                raise StopIteration
        else:
            if method in ('M-SEARCH', 'NOTIFY'):
                self.id = None
                self.method, self.path, self.version = method, path, version
                #self.requestline = f'{method} {path} {version}'
                self.requestline = '{0} {1} {2}'.format(method, path, version)
                self.build()
            else:
                raise StopIteration
        try:
            self.addr = address(*addr)
        except TypeError:
            self.addr = None

        #self.headers = {'st': f'{library}:{service}', 'mx': mx, 'man': '"ssdp:discover"', 'host': f'{host}:{port}'}
        self.headers = {'st': '{0}:{1}'.format(library, service), 'mx': mx, 'man': '"ssdp:discover"', 'host': '{0}:{1}'.format(host, port)}
    def build(self, service='rootdevice', library='upnp', host=ssdpaddr.host, port=ssdpaddr.port, mx='3'):
        return self


class REPLY(BASE, dict):
    def __init__(self, message, addr):
        message = message.rstrip().splitlines()
        self.statusline = message[0].decode('latin-1')
        self.version, self.code, self.codemsg = self.statusline.split()
        if self.code in ('200',):
            headers = b"\r\n".join(message[1:])
            self.headers = getheaders(headers)
            try:
                self.id = uuid.UUID(self.headers['USN'].split('::')[0])
            except KeyError:
                self.id = None
        self.addr = address(*addr)


if __name__ == '__main__':
    import pprint

    request = REQUEST(bytes(REQUEST()))

    print(request)
    print(repr(request))

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
    print(reply)
