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
      def protocolflow(self, out_port):
          msg = of.ofp_flow_mod()
          msg.match = of.ofp_match.from_packet(packet)    
          msg.data = packet_in
          msg.idle_timeout = 30
          msg.hard_timeout = 30
          action = of.ofp_action_output(port = out_port)
          msg.actions.append(action)
          self.connection.send(msg)


      def drop(self, op, ipsrc):
          msg = of.ofp_flow_mod()
          match = of.ofp_match()
          match.icmp_type = op
          match.nw_src = ipsrc
            	  
          msg.match = match
          msg.idle_timeout = 10
          msg.hard_timeout = 100
          self.connection.send(msg)
      
                     
      def dropANY(duration =None):
          msg = of.ofp_flow_mod()
          match = of.ofp_match()
          msg.match = match
          msg.idle_timeout = 30
          msg.hard_timeout = 100
          self.connection.send(msg)
             
      get_ARP = packet.find('arp')
      get_ICMP = packet.find('icmp')
      get_IPv4 = packet.find('ipv4')
 
      if get_ARP:
         protocolflow(self, of.OFPP_ALL)
      elif get_IPv4:
         if switch_id == 1:
            if port_on_switch == 1: 
               protocolflow(self, 2)
            elif port_on_switch ==2:
               protocolflow(self,1)   
         elif switch_id==2: 
              if port_on_switch == 1:
                 protocolflow(self, 2)
              elif port_on_switch == 2:
                 protocolflow(self, 1)
         elif switch_id==3:
            if port_on_switch == 1:
               protocolflow(self, 2)
            elif port_on_switch == 2:
               protocolflow(self, 1)
         elif switch_id==4:
           if port_on_switch == 1: 
              protocolflow(self, 2)
           elif port_on_switch == 2:
              protocolflow(self, 1)
         elif switch_id==5:
            if port_on_switch == 5 and get_IPv4.srcip=='128.114.50.10':
              if get_ICMP:
                 if get_ICMP.type ==8:
                    drop(self, 8, None)
                 else:
                    protocolflow(self,of.OFPP_ALL)
              elif get_IPv4.srcip == '128.114.50.10' and get_IPv4.dstip == '10.0.4.104':
                 dropANY()
              elif get_IPv4.srcip == '10.0.4.104' and get_IPv4.dstip == '128.114.50.10':
                 dropANY()
              else:
                 protocolflow(self, of.OFPP_ALL)
             
            else:
              protocolflow(self, of.OFPP_ALL)
           #protocolflow(self,port_on_switch)
          # protocolflow(self,2)
          # protocolflow(self,3)
          # protocolflow(self,4)
          # protocolflow(self,5)   
        # else:
          # drop()

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
