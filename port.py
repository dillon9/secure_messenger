import miniupnpc
port = 5005
proto = "TCP"
description = "Python p2p chat"

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 10
upnp.discover()
upnp.selectigd()

try:
	upnp.addportmapping(port, proto, upnp.lanaddr, port, description, '')
except Exception, e:
	print "Unable to add UPnP port mapping. ", e
