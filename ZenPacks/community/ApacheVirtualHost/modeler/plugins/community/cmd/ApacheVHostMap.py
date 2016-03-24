from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class ApacheVHostMap(CommandPlugin):
    relname = 'virtualHosts'
    command = "/usr/sbin/apachectl -S 2>&1"
    modname = 'ZenPacks.community.ApacheVirtualHost.VirtualHost'
    
    def process(self, device, results, log):
        log.info('Collecting Apache Virtual Host information for device %s' % device.id)

        rm = self.relMap()

        data = results.splitlines()

        defaults = False

        for line in data:
            if line.startswith('VirtualHost configuration'):
                continue

            if line.startswith('wildcard NameVirtualHosts'):
                defaults = True
                continue

            if line.startswith('Syntax'):
                continue 

            elems = line.split()
            ip = elems[0].split(':')[0]
            port = elems[0].split(':')[1]
            hostname = elems[1]
            protocol = 'http'
            if port == '443':
              protocol = 'https'

            rm.append(self.objectMap({
                'id': self.prepId(hostname),
                'title': hostname,
                'ip': ip,
                'port': port,
                'protocol': protocol,
                }))

        return rm
