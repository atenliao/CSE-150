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
     def protocolflow(self, nw_proto, dl_type, ipsrc, ipdst):
         msg = of.ofp_flow_mod()
         match = of.ofp_match()
         match.nw_src = ipsrc
         match.nw_dst = ipdst
         match.tp_src = None
         match.tp_dst = None
         match.nw_proto = nw_proto
         match.dl_type = dl_type
         msg.match = match
         msg.hard_timeout = 0
         msg.soft_timeout = 0
         msg.priority = 32768
         action = of.ofp_action_output(port = of.OFPP_NORMAL)
         msg.actions.append(action)
         # if (PRINT_PACKET_CONTENTS):
         #    print "Inserting flow for protocol: " + msg.__str__()
         self.connection.send(msg)

     def drop(duration = None):
       
            #msg.in_port = packet.port
           # self.connection.send(msg)
         msg = of.ofp_flow_mod()
         match = of.ofp_match()
         msg.match = match
         msg.hard_timeout =0
         msg.soft_timeout =0
         msg.priority = 1
         self.connection.send(msg)
         
         
   # def flood (message = None):
   #    msg = of.ofp_packet_out()
   #    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
   #    self.connection.send(msg)

     if packet.type == packet.ARP_TYPE:
        
        protocolflow(self,None,packet.ARP_TYPE, None, None)
        #protocolflow(self,  packet.ARP_TYPE)
        print "ARP success"
     elif packet.type == packet.IP_TYPE:
          print "IP_TYPE test"
          IP_packet = packet.payload
         #if IP_packet.protocol == IP_packet.TCP_PROTOCOL:
         #     protocolflow(self, None, None)
        #      print "TCP test"
         # if IP_packet.protocol == IP_packet.ICMP_PROTOCOL:
          ip = packet.find('ipv4')
              #print "Source IP:", ip.srcip
              #print "Desctination IP:", ip.dstip
          if IP_packet.protocol == IP_packet.TCP_PROTOCOL:
              protocolflow(self, IP_packet.TCP_PROTOCOL, packet.IP_TYPE, None,None)
          elif IP_packet.protocol == IP_packet.ICMP_PROTOCOL:
             print "match ICMP PROTOCOL"
            # print "Source ip: ", ip.srcip
            # print "Dist   ip: ", ip.dstip  
            # protocolflow(self, IP_packet.ICMP_PROTOCOL, packet.IP_TYPE, None,None)
             if ip.srcip == "10.0.1.10" and ip.dstip == "10.0.1.40":
                print "Source ip: ", ip.srcip
                print "Dist   ip: ", ip.dstip 
                protocolflow(self, None, packet.IP_TYPE, None, None)
             elif ip.srcip == "10.0.1.40" and ip.dstip == "10.0.1.10":
                print "Source ip: ", ip.srcip
                print "Dist   ip: ", ip.dstip
                protocolflow(self, None, packet.IP_TYPE, None, None)
                print "ICMP test"
             else:
                drop()
                print "drop packet srcip"
                msg.priority = 32768   
          else:
             drop()
             print "drop any any"
             msg.priority = 32768
           #if IP_packet.protocol == IP_packet.TCP_PROTOCOL:
           #     protocolflow(self,IP_packet.TCP_PROTOCOL, packet.IP_TYPE, None, None)
            # drop()
            # print "Drop test"

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
