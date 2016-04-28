from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class ApacheVHostMap(CommandPlugin):
    relname = 'virtualHosts'
    command = "/usr/sbin/apachectl -S 2>&1"
    modname = 'ZenPacks.community.ApacheVirtualHost.VirtualHost'

    def process(self, device, results, log):
        log.info('Collecting Apache Virtual Host information for device %s' % device.id)

        relmap = self.relMap()

        data = results.splitlines()

        nameip = ""
        nameport = ""

        for line in data:
            hostname = ""
            port = ""
            hosttype = ""
            ipaddr = ""

            if "Syntax error" in line:
                log.error('Syntax error from apachectl, check config and if user has sufficient permissions')
                break

            if "VirtualHost configuration" in line:
                continue

            if '[warn]' in line:
                continue

            if 'alias' in line:
                continue

            if 'Could not reliably deetermine' in line:
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
                hosttype = "Name Based"
                ipaddr = nameip
            elif line.startswith("default server"):
                elems = line.split()
                hostname = elems[2]
                port = nameport
                hosttype = "Name Based"
                ipaddr = nameip
            elif line.startswith("ServerRoot"):
                break
            else:
                elems = line.split()
                hostname = elems[1]
                ipaddr = elems[0].split(':')[0]
                port = elems[0].split(':')[1]
                hosttype = "IP Based"

            protocol = 'http'
            if port == '443':
                protocol = 'https'

            if port == '*':
                port = '80'

            relmap.append(self.objectMap({
                'id': self.prepId(hostname),
                'title': hostname,
                'ip': ipaddr,
                'port': port,
                'protocol': protocol,
                'type':hosttype,
                }))

        return relmap
