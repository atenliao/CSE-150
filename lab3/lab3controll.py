# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
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

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
     print "Example Code."
     def protocolflow(self, nw_priority ):
         msg = of.ofp_flow_mod()
         #match = of.ofp_match()
         #match.from_packet = packet
         #match.nw_proto = proto
         #match.dl_type = dl_type
         msg.match = of.ofp_match.from_packet(packet)
         #msg.match = match
        
         msg.data = packet_in
         msg.idle_timeout = 10
         msg.hard_timeout = 30
         msg.priority = nw_priority
         action = of.ofp_action_output(port = of.OFPP_FLOOD)
         msg.actions.append(action)
         self.connection.send(msg)

     def drop(duration = None):
        # if duration is not None:
          # if not isinstance(duration, tuple):
           #   duration = (duration, duration)
           #msg.in_port = packet.port
           # self.connection.send(msg)
           msg = of.ofp_flow_mod()
          # msg = of.ofp_packet_out()
           match = of.ofp_match.from_packet(packet)
           msg.match = match
          # msg.actions.append(of.ofp_action_output())
           msg.idle_timeout =30
           msg.hard_timeout =50
           #msg.buffer_id = ofp.buffer_id
        # msg.priority = 1
           self.connection.send(msg)
         
         
   # def flood (message = None):
   #    msg = of.ofp_packet_out()
   #    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
   #    self.connection.send(msg)
     get_ARP = packet.find('arp')
     get_TCP = packet.find('tcp')
     get_ICMP = packet.find("icmp")
     get_ipv4 = packet.find('ipv4')
     if get_ARP:
       protocolflow(self, 1000)
       print "ARP PASS" 
 
     elif get_TCP or get_ipv4:
       # protocolflow()
        print "TCP and ipv4 pass"
        if  not get_ICMP:
           protocolflow(self, 32768)
           print "pass not ICMP"
        else:
           if get_ipv4.srcip == "10.0.1.10" and get_ipv4.dstip == "10.0.1.40":
              print "Source:", get_ipv4.srcip
              print "Dst   :", get_ipv4.dstip         
              protocolflow(self, 10)
              print "drop packet 10"
           elif get_ipv4.srcip == "10.0.1.40" and get_ipv4.dstip == "10.0.1.10":
              protocolflow(self, 10)
              print "packet 2 test"
           else:
              drop()
              print "drop packet not match"  
     else:
         drop()
         # msg = of.ofp_packet_out()
         # self.connection.send(msg)
         print "drop any any"
            # msg.priority = 32768       

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
