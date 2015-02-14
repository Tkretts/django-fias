# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from fias.models import Version

from suds.client import Client
from suds.transport.http import HttpTransport


class WellBehavedHttpTransport(HttpTransport):
    """ HttpTransport which properly obeys the ``*_proxy``
        environment variables.
    """

    def u2handlers(self):
        """ Return a list of specific handlers to add.

            The urllib2 logic regarding ``build_opener(*handlers)`` is:

            - It has a list of default handlers to use

            - If a subclass or an instance of one of those default handlers
                is given in ``*handlers``, it overrides the default one.

            Suds uses a custom {'protocol': 'proxy'} mapping in self.proxy, and
            adds a ProxyHandler(self.proxy) to that list of handlers.
            This overrides the default behaviour of urllib2, which would
            otherwise use the system configuration (environment variables
            on Linux, System Configuration on Mac OS, ...) to determine which
            proxies to use for the current protocol, and when not to use
            a proxy (no_proxy).

            Thus, passing an empty list will use the default ProxyHandler which
            behaves correctly.
        """
        return []


def fetch_version_info(update_all=False):
    client = Client(
        url="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL",
        transport=WellBehavedHttpTransport())
    result = client.service.GetAllDownloadFileInfo()

    for item in result.DownloadFileInfo:
        try:
            ver = Version.objects.get(ver=item['VersionId'])
        except Version.DoesNotExist:
            ver = Version(**{
                'ver': item['VersionId'],
                'dumpdate': datetime.datetime.strptime(
                    item['TextVersion'][-10:], "%d.%m.%Y").date(),
            })
        finally:
            if not ver.pk or update_all:
                setattr(ver, 'complete_xml_url', item['FiasCompleteXmlUrl'])
                if hasattr(item, 'FiasDeltaXmlUrl'):
                    setattr(ver, 'delta_xml_url', item['FiasDeltaXmlUrl'])
                else:
                    setattr(ver, 'delta_xml_url', None)
                ver.save()
