#!/usr/bin/python

"""Topology with 10 switches and 10 hosts
"""

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import setLogLevel

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class CSLRTopo( Topo ):

        def __init__( self ):
                "Create Topology"

                # Initialize topology
                Topo.__init__( self )

                # Add hosts
                alice = self.addHost( 'alice' )
                bob = self.addHost( 'bob' )
                carol = self.addHost( 'carol' )

                # Add routers
                robert = self.addNode( 'robert', cls=LinuxRouter )
                richard = self.addNode( 'richard', cls=LinuxRouter )
                rupert = self.addNode( 'rupert', cls=LinuxRouter )

                # Add switches
                s0 = self.addSwitch( 's0', listenPort=6634 )
                s1 = self.addSwitch( 's1', listenPort=6635 )
                s2 = self.addSwitch( 's2', listenPort=6636 )

                # Add links between hosts and switches
                self.addLink( alice, s0 ) # alice-eth0 <-> s0-eth1
                self.addLink( bob, s1 ) # bob-eth0 <-> s1-eth1
                self.addLink( carol, s2 ) # carol-eth0 <-> s2-eth1

                # Add links between router and switches
                self.addLink( s0, robert )  # robert-eth0 <-> s0-eth2
                self.addLink( s1, robert )  # robert-eth1 <-> s1-eth2
                self.addLink( s1, richard )  # richard-eth0 <-> s1-eth3
                self.addLink( s2, richard )  # richard-eth1 <-> s2-eth2
                self.addLink( s2, rupert )  # rupert-eth0 <-> s2-eth3 


def run():
        "Create and configure network"
        topo = CSLRTopo()
        net = Mininet( topo=topo, link=TCLink, controller=None )

        # Set interface IP and MAC addresses for hosts
        alice = net.get( 'alice' )
        alice.intf( 'alice-eth0' ).setIP( '10.1.1.17', 24 )
        alice.intf( 'alice-eth0' ).setMAC( '0A:00:00:02:00:00' )

        bob = net.get( 'bob' )
        bob.intf( 'bob-eth0' ).setIP( '10.4.4.48', 24 )
        bob.intf( 'bob-eth0' ).setMAC( '0A:00:01:02:00:00' )

        carol = net.get( 'carol' )
        carol.intf( 'carol-eth0' ).setIP( '10.6.6.69', 24 )
        carol.intf( 'carol-eth0' ).setMAC( '0A:00:03:02:00:00' )

        # Set interface IP and MAC addresses for router
        robert = net.get( 'robert' )
        robert.intf( 'robert-eth0' ).setIP( '10.1.1.14', 24 )
        robert.intf( 'robert-eth0' ).setMAC( '0A:00:0B:01:00:03' )
        robert.intf( 'robert-eth1' ).setIP( '10.4.4.14', 24 )
        robert.intf( 'robert-eth1' ).setMAC( '0A:00:0C:01:00:03' )

        richard = net.get( 'richard' )
        richard.intf( 'richard-eth0' ).setIP( '10.4.4.46', 24 )
        richard.intf( 'richard-eth0' ).setMAC( '0A:00:02:01:00:01' )
        richard.intf( 'richard-eth1' ).setIP( '10.6.6.46', 24 )
        richard.intf( 'richard-eth1' ).setMAC( '0A:00:0B:FE:00:02' )

        rupert = net.get( 'rupert' )
        rupert.intf( 'rupert-eth0' ).setIP( '10.6.6.254', 24 )
        rupert.intf( 'rupert-eth0' ).setMAC( '0A:00:0D:FE:00:02' )


        # Set interface MAC address for switches (NOTE: IP
        # addresses are not assigned to switch interfaces)
        s0 = net.get( 's0' )
        s0.intf( 's0-eth1' ).setMAC( '0A:00:00:01:00:01' )
        s0.intf( 's0-eth2' ).setMAC( '0A:00:0A:01:00:02' )
        
        s1 = net.get( 's1' )
        s1.intf( 's1-eth1' ).setMAC( '0A:00:01:01:00:01' )
        s1.intf( 's1-eth2' ).setMAC( '0A:00:0A:FE:00:02' )
        s1.intf( 's1-eth3' ).setMAC( '0A:00:0E:01:00:03' )

        s2 = net.get( 's2' )
        s2.intf( 's2-eth1' ).setMAC( '0A:00:0C:FE:00:04' )
        s2.intf( 's2-eth2' ).setMAC( '0A:00:0D:01:00:03' )
        s2.intf( 's2-eth3' ).setMAC( '0A:00:03:01:00:01' )

        net.start()

        # Add routing table entries for hosts (NOTE: The gateway
		# IPs 10.0.X.1 are not assigned to switch interfaces)
        alice.cmd( 'route add default gw 10.1.1.1 dev alice-eth0' )
        bob.cmd( 'route add default gw 10.4.4.1 dev bob-eth0' )
        carol.cmd( 'route add default gw 10.6.6.1 dev carol-eth0' )
        
        bob.cmd( 'ip route add 10.1.1/24 via 10.4.4.1 dev bob-eth0' )
        carol.cmd( 'route add 10.1.1/24 via 10.6.6.1 dev carol-eth0' )
        carol.cmd( 'route add 10.4.4/24 via 10.6.6.1 dev carol-eth0' )

        #robert.cmd( 'route add default gw 10.4.4.2 dev robert-eth1' )
        #robert.cmd ( 'ip route add 10.4.4.48 via 10.4.4.2 dev robert-eth1' )
        robert.cmd ( 'ip route add 10.6.6/24 via 10.4.4.2 dev robert-eth1' )
        robert.cmd ( 'ip route change 10.1.1/24 via 10.1.1.2 dev robert-eth0' )
        robert.cmd ( 'ip route change 10.4.4/24 via 10.4.4.2 dev robert-eth1' )
        

        #richard.cmd( 'route add default gw 10.4.4.3 dev richard-eth0' )
        richard.cmd ( 'ip route add 10.1.1/24 via 10.4.4.3 dev richard-eth0' )
        richard.cmd ( 'ip route change 10.4.4/24 via 10.4.4.3 dev richard-eth0' )
        richard.cmd ( 'ip route change 10.6.6/24 via 10.6.6.2 dev richard-eth1' )

        rupert.cmd ( 'ip route add 10.1.1/24 via 10.6.6.3 dev rupert-eth0' )
        rupert.cmd ( 'ip route add 10.4.4/24 via 10.6.6.3 dev rupert-eth0' )
        rupert.cmd ( 'ip route change 10.6.6/24 via 10.6.6.3 dev rupert-eth0' )

        # Add arp cache entries for hosts
        alice.cmd( 'arp -s 10.1.1.1 0A:00:00:01:00:01 -i alice-eth0' )
        bob.cmd( 'arp -s 10.4.4.1 0A:00:01:01:00:01 -i bob-eth0' )
        carol.cmd( 'arp -s 10.6.6.1 0A:00:0C:FE:00:04 -i carol-eth0' )
        robert.cmd( 'arp -s 10.1.1.2 0A:00:0A:01:00:02 -i robert-eth0' )
        robert.cmd( 'arp -s 10.4.4.2 0A:00:0A:FE:00:02 -i robert-eth1' )
        richard.cmd( 'arp -s 10.4.4.3 0A:00:0E:01:00:03 -i richard-eth0' )
        richard.cmd( 'arp -s 10.6.6.2 0A:00:0D:01:00:03 -i richard-eth1' )
        rupert.cmd( 'arp -s 10.6.6.3 0A:00:03:01:00:01 -i rupert-eth0' )
        # Open Mininet Command Line Interface
        CLI(net)

        # Teardown and cleanup
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
