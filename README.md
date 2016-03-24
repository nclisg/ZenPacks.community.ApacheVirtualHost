Assign the modeler plugin to any device under /server and it will model then monitor the Virtual Hosts

Monitoring template requires nagios check_http plugin


Any sites running on 443 will be monitored as HTTP and they will have the TLS certificate checked and events raised if the expiry time is 30 days or less
