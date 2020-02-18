#! /usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

class MyTopology(Topo):
	"""
	A basic topology
	"""
	def __init__(self):
	  Topo.__init__(self)
	  n=6
	  #Set up Topology Here
	  switch1 = self.addSwitch('s1')
	  switch2 = self.addSwitch('s2')
	  switch3 = self.addSwitch('s3')
	  for h in range(n):
	  	host = self.addHost('h%s' % (h+1))
	  	if h==0 or h==2:
		   self.addLink(host,switch1)
		elif h==1 or h==3:
		   self.addLink(host,switch2)
		elif h==4 or h==5:
		   self.addLink(host,switch3)
	  
	  self.addLink(switch1,switch3)
	  self.addLink(switch3,switch2)
if __name__ == '__main__':
	"""
	If this script is run as an executable (by chmod +x), this is 
	what it will do
	"""

	topo = MyTopology()
	net = Mininet(topo = topo)
	net.start()

	CLI(net)

	net.stop()
