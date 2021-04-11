# Part D

i. Describe how OpenFlow protocol can be used to place h2 as a middle box for modifying the UDP traffic between h1 and h0.

A flow rule can be installed on the switch such that if it sees the packet is sent from h0 and destined to h1 and is of UDP, it should first route it to h2 to encrypt the message. Similarly if the packet is sent from h1 and destined to h0 is of UDP, the switch should first route the message to h2 for encryption. If the message is arrived from h2, then it could just forward it straight to the corresponding destination. 

ii. Write the OpenFlow rules to implement your approach.

```
ovs-ofctl -O OpenFlow13 add-flow in_port=1,udp,nw_src=10.0.0.100,nw_dst=10.0.0.101,actions=output=3

ovs-ofctl -O OpenFlow13 add-flow in_port=3,udp,nw_src=10.0.0.102,nw_dst=10.0.0.101,actions=output=2

ovs-ofctl -O OpenFlow13 add-flow in_port=3,udp,nw_src=10.0.0.102,nw_dst=10.0.0.100,actions=output=1

ovs-ofctl -O OpenFlow13 add-flow in_port=2,udp,nw_src=10.0.0.101,nw_dst=10.0.0.100,actions=output=3
```

iii. Explain what the network function running in h2 will look like i.e. what actions does it perform when it receives a new packet. You can outline the program running in h2 in a pseudo-code4

The steps that h2 will need to take
- Receive IP packet
- Save the destination address in the IP packet, so we know the host to send the packet to.
- Decapsulate the IP packet to get the UDP segment. Here we need to save the source and destination port number so we know which port to forward the packet to. We also need to save the time to live since we shouldn't refresh the TTL when sending the packet out again.
- Then we need to decapsulate the UDP segment to actual application payload and apply the encrpytion on the application layer
- When sending out the message, the message will be encapsulated into a UDP segment and the length, checksum will be recomputed based on the newly encrpyted data. However the source and destination port number that's been stored will be inserted in the header.
- Then the UDP segment will be encapsulated into an IP datagram. Some fields like length will be recomputed with the new length. Other fields like dest IP addr and TTL will be inserte with the stored values. The IP datagram then gets sent out.
