# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
      #print "Hello, World!"
      def protocolflow(self, out_port, proto, dl_type):
          msg = of.ofp_flow_mod() 
          match = of.ofp_match.from_packet(packet)
          match.nw_proto = proto
          match.dl_type = dl_type
          match.tp_src = None
          match.tp_dst = None
          match.nw_tos = None
          msg.match = match    
          msg.data = packet_in
          msg.idle_timeout = 30
          msg.hard_timeout = 50
          action = of.ofp_action_output(port = out_port)
          msg.actions.append(action)
          self.connection.send(msg)

      def drop(self, proto,dl_type, ipsrc, ipdst):  
      #def drop(self, op, ipsrc, ipdst):
          msg = of.ofp_flow_mod()
          match = of.ofp_match.from_packet(packet)
         # match.icmp_type = op
          match.ip__proto = proto
          match.dl_type = dl_type
          match.nw_src = ipsrc
          match.nw_dst = ipdst
          match.nw_tos = None  	  
          msg.match = match
          msg.idle_timeout = 10
          msg.hard_timeout = 100
          self.connection.send(msg)
      
                     
      def dropANY(self, ipsrc, ipdst):
          msg = of.ofp_flow_mod()
          match = of.ofp_match.from_packet(packet)
          match.nw_src = ipsrc
	  match.nw_dst = ipdst
          match.nw_tos = None
          msg.match = match
          msg.idle_timeout = 30
          msg.hard_timeout = 100
          self.connection.send(msg)
             
      get_ARP = packet.find('arp')
      get_ICMP = packet.find('icmp')
      get_IPv4 = packet.find('ipv4')
 
      if get_ARP:
         protocolflow(self, of.OFPP_FLOOD,None, packet.ARP_TYPE)
      elif get_IPv4:
         if switch_id == 1:
              if port_on_switch == 1: 
                 protocolflow(self, 2,None,packet.IP_TYPE)
              elif port_on_switch ==2:
                 protocolflow(self,1,None,packet.IP_TYPE)   
         elif switch_id==2: 
              if port_on_switch == 1:
                 protocolflow(self, 2,None,packet.IP_TYPE)
              elif port_on_switch == 2:
                 protocolflow(self, 1,None,packet.IP_TYPE)
         elif switch_id==3:
              if port_on_switch == 1:
                 protocolflow(self, 2,None,packet.IP_TYPE)
              elif port_on_switch == 2:
                 protocolflow(self, 1,None,packet.IP_TYPE)
         elif switch_id==4:
              if port_on_switch == 1: 
                 protocolflow(self, 2,None,packet.IP_TYPE)
              elif port_on_switch == 2:
                 protocolflow(self, 1,None,packet.IP_TYPE)
         elif switch_id==5:             
            if port_on_switch ==5:
              print "srcip is ",get_IPv4.srcip
              if get_ICMP:
                    print "icmp"
                    drop(self, 1,packet.IP_TYPE,"128.114.50.0/24",None)
              elif get_IPv4.srcip == '128.114.50.10' and get_IPv4.dstip == '10.0.4.104':
                 dropANY(self,"128.114.50.0/24","10.0.4.0/24")
              elif get_IPv4.srcip == '10.0.4.104' and get_IPv4.dstip == '128.114.50.10':
                 dropANY(self,"10.0.4.0/24","128.114.50.0/24")
              else:
                 protocolflow(self, of.OFPP_ALL,None,None)
             
            else:
              protocolflow(self, of.OFPP_ALL,None,None)
           

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
