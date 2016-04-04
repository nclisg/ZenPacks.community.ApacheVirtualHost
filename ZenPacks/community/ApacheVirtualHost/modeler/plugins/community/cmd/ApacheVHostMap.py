from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
import re

class ApacheVHostMap(CommandPlugin):
    relname = 'virtualHosts'
    command = "/usr/sbin/apachectl -S 2>&1"
    modname = 'ZenPacks.community.ApacheVirtualHost.VirtualHost'
    
    def process(self, device, results, log):
        log.info('Collecting Apache Virtual Host information for device %s' % device.id)

        rm = self.relMap()

        data = results.splitlines()

        defaults = False
   
        nameip = ""
        nameport = ""

        for line in data:
            hostname = ""
            port = ""
            type = ""

            if "Syntax error" in line:
                log.error('Syntax error from apachectl, check config and if user has sufficient permissions')
                
                break;

            if "VirtualHost configuration" in line:
                continue

            if line.startswith("Syntax"):
                continue

            if "is a NameVirtualHost" in line:
                elems = line.split()
                nameip = elems[0].split(':')[0]
                nameport = elems[0].split(':')[1]
                continue

            if line.startswith("wildcard NameVirtualHosts"):
                continue

            if line.startswith("wildcard"):
                continue

            if "namevhost" in line:
                elems = line.split()
                hostname = elems[3]
                port = elems[1]
                type = "Name Based"
                ip = nameip
            elif line.startswith("default server"):
                elems = line.split()
                hostname = elems[2]
                port = nameport
                type = "Name Based"
                ip = nameip
            else:
                elems = line.split()
                hostname = elems[1]
                ip = elems[0].split(':')[0]
                port = elems[0].split(':')[1]
                type = "IP Based"
                

            protocol = 'http'
            if port == '443':
                protocol = 'https'

            rm.append(self.objectMap({
                'id': self.prepId(hostname),
                'title': hostname,
                'ip': ip,
                'port': port,
                'protocol': protocol,
                'type':type,
                }))

        return rm
