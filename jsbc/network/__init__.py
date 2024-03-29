# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import os
import contextlib
from jsbc.compat.python3 import *
from jsbc.compat.urllib.urlopen import urlopen
from jsbc.compat.urllib.Request import Request
from jsbc.compat.urllib.HTTPError import HTTPError
from jsbc.compat.urllib.URLError import URLError
from jsbc.compat.urllib.build_opener import build_opener
from jsbc.compat.urllib.urlparse import urlparse
from jsbc.compat.pathlib import pathlib
import time
from jsbc.compat.pickle import pickle as cPickle
import bz2
from jsbc.Toolbox import SettingsClass, DefaultSettings, settings

import logging
logger = logging.getLogger(__name__)

__version__ = '0.0.0'

settingsDefaults = [
    ('client', [
        ('name', __name__),
        ('cache path', '%TEMP%/jsbc.cache'),
        ('network', [
            ('User-Agent', "{0}/{1} {2}".format(__name__, __version__, build_opener().addheaders[0][1])),
        ]),
    ]),
]


def DownloadPage(URL, hdr):
    """ """ # TODO
    try:
        with contextlib.closing(urlopen(Request(URL, headers=hdr))) as Builtins:
            encoding = Builtins.headers['content-type'].split('charset=')[-1]
            Actions = Builtins.read()
            try:
                Actions = str(Actions, encoding)
            except LookupError:
                pass

    except (HTTPError, URLError) as err:
        if err.code == 304:
            Result = {'Code': err.code}
        else:
            print('{0}: Error: Can\'t connect to "{1}".'.format(Settings['client']['name'], URL)) # TODO
            raise
    except Exception:
        logger.exception('%s, %s', URL, hdr)
        raise
    else:
        try:
            CacheExpire = time.time() + int(next(x for x in Builtins.headers['Cache-Control'].split(',') if 'max-age' in x).split('=')[1])
        except (KeyError, AttributeError):
            CacheExpire = None
        #Result = {'Code': Builtins.getcode(), 'Page': Actions, 'Cache-Expire': time.time() + int(next(x for x in Builtins.headers['Cache-Control'].split(',') if 'max-age' in x).split('=')[1])}
        Result = {'Code': Builtins.getcode(), 'Page': Actions, 'Cache-Expire': CacheExpire}
        try:
            if Builtins.headers['ETag'] != None:
                Result['ETag'] = Builtins.headers['ETag']
        except:
            pass
        try:
            if Builtins.headers['Last-Modified'] != None:
                Result['Last-Modified'] = Builtins.headers['Last-Modified']
        except:
            pass

    return Result


def DownloadURL(URL, force=False, cached=False): # TODO
    """ """  # TODO
    try:
        DownloadURL.URLCache
    except AttributeError:
        try:
            with (CachePath / 'URLCache.bz2').open('rb') as f:
                DownloadURL.URLCache = cPickle.loads(bz2.decompress(f.read()))
        except Exception:
            logger.exception('')
            DownloadURL.URLCache = {}
    finally:
        URLCache = DownloadURL.URLCache

    hdr = {'User-Agent': Settings['client']['network']['User-Agent']}
    SaveCache = False

    if urlparse(URL).scheme in ('file', ''):
        with open(urlparse(URL).path, 'rb') as f:
            Actions = {'Page': f.read()}
    else:
        if cached and URL in URLCache:
            Actions = URLCache[URL]
        elif not force and URL in URLCache and 'Cache-Expire' in URLCache[URL] and URLCache[URL]['Cache-Expire']:
            if time.time() > URLCache[URL]['Cache-Expire']:
                try:
                    hdr['If-None-Match'] = URLCache[URL]['ETag']
                except KeyError:
                    pass
                try:
                    hdr['If-Modified-Since'] = URLCache[URL]['Last-Modified']
                except KeyError:
                    pass
                Actions = DownloadPage(URL, hdr)
                if Actions['Code'] == 304:
                    Actions = URLCache[URL]
                elif Actions['Code'] == 200:
                    SaveCache = True
                else:
                    print("Unknown code:", Actions['Code']) # TODO
            else:
                Actions = URLCache[URL]
        else:
            Actions = DownloadPage(URL, hdr)
            SaveCache = True

    if SaveCache:
        URLCache[URL] = Actions
        CachePath.mkdir(parents=True, exist_ok=True)
        with (CachePath / 'URLCache.bz2').open('wb') as f:
            f.write(bz2.compress(cPickle.dumps(URLCache,2)))

    return Actions['Page']


DefaultSettings(settingsDefaults)
Settings = settings
CachePath = pathlib.Path(os.path.expandvars(settings['client']['cache path']))