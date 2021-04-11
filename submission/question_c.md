# Part C

i. Try pinging from h1 to h5. The ping should succeed, despite the fact that you have not installed any rules on the switches yourself. Study the output of the POX program, what has the controller done? Include the DEBUG output as well as your interpretation of it.

DEBUG pox output:
```
POX 0.3.0 (dart) / Copyright 2011-2014 James McCauley, et al.
DEBUG:core:POX 0.3.0 (dart) going up...
DEBUG:core:Running on CPython (2.7.18/Mar 8 2021 13:02:45)
DEBUG:core:Platform is Linux-5.4.0-70-generic-aarch64-with-Ubuntu-20.04-focal
INFO:core:POX 0.3.0 (dart) is up.
DEBUG:openflow.of_01:Listening on 0.0.0.0:6633

INFO:openflow.of_01:[00-00-00-00-00-07 6] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-07 6]
INFO:openflow.of_01:[00-00-00-00-00-06 3] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-06 3]
INFO:openflow.of_01:[00-00-00-00-00-01 2] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-01 2]
INFO:openflow.of_01:[00-00-00-00-00-02 5] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-02 5]
INFO:openflow.of_01:[00-00-00-00-00-04 7] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-04 7]
INFO:openflow.of_01:[00-00-00-00-00-03 4] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-03 4]
INFO:openflow.of_01:[00-00-00-00-00-05 8] connected
DEBUG:forwarding.l2_learning:Connection [00-00-00-00-00-05 8]
DEBUG:openflow.of_01:1 connection aborted

DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.1 -> 00:00:00:00:00:01.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.1 -> 00:00:00:00:00:01.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.2 -> 00:00:00:00:00:01.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.3 -> 00:00:00:00:00:01.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.3 -> 00:00:00:00:00:01.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:01.1 -> 00:00:00:00:00:05.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:01.1 -> 00:00:00:00:00:05.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:01.1 -> 00:00:00:00:00:05.2
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:01.3 -> 00:00:00:00:00:05.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:01.3 -> 00:00:00:00:00:05.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.1 -> 00:00:00:00:00:01.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.1 -> 00:00:00:00:00:01.3
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.2 -> 00:00:00:00:00:01.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.3 -> 00:00:00:00:00:01.1
DEBUG:forwarding.l2_learning:installing flow for 00:00:00:00:00:05.3 -> 00:00:00:00:00:01.1
```

In the POX output, we see that when we first create the network topology, the controller will try to connect to each of the switches (00-00-00-00-0x) created (x from 1 to 7). 

When we try to `h1 ping h5`, as suggested from the DEBUG logs, POX is trying to install the flow rules on each of the switches so that the switch will know where to forward the received packet. These rules will have to include both the sending of the ping (an echo request), as well as the receiving of the ping (an echo reply)


ii. Record the ping RTT times for the first 10 ping messages. Compare the RTT of the first ping message with the subsequent ones. Is there a difference? Why or why not?

```
mininet> h1 ping h5 -c 10
PING 10.0.0.5 (10.0.0.5) 56(84) bytes of data.
64 bytes from 10.0.0.5: icmp_seq=1 ttl=64 time=50.0 ms
64 bytes from 10.0.0.5: icmp_seq=2 ttl=64 time=2.83 ms
64 bytes from 10.0.0.5: icmp_seq=3 ttl=64 time=0.150 ms
64 bytes from 10.0.0.5: icmp_seq=4 ttl=64 time=0.281 ms
64 bytes from 10.0.0.5: icmp_seq=5 ttl=64 time=0.258 ms
64 bytes from 10.0.0.5: icmp_seq=6 ttl=64 time=0.166 ms
64 bytes from 10.0.0.5: icmp_seq=7 ttl=64 time=0.213 ms
64 bytes from 10.0.0.5: icmp_seq=8 ttl=64 time=0.116 ms
64 bytes from 10.0.0.5: icmp_seq=9 ttl=64 time=0.258 ms
64 bytes from 10.0.0.5: icmp_seq=10 ttl=64 time=0.196 ms

--- 10.0.0.5 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9170ms
rtt min/avg/max/mdev = 0.116/5.445/49.984/14.867 ms
```

As seen from logs above, the subsequent RTTs are shorter than the RTT for the first ping. This is because in the first ping, the controller needs to compute a route to route the message from h1 and h5 and install the flow rules on the switches on the route. The timeframe makes sense (in ms) since the control plane operates in milliseconds. However once the rules are installed on the switches, we do not need to reinstall it again until it expires, hence the shorter RTT for rest of the pings.

iii.

In `s1`:
```
ovs-ofctl dump-flows s1
cookie=0x0, duration=3.908s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s1-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:05,nw_src=10.0.0.1,nw_dst=10.0.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s1-eth2"
cookie=0x0, duration=3.894s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s1-eth2",vlan_tci=0x0000,dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.5,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s1-eth1"
```

In `s2`:
```
ovs-ofctl dump-flows s2
cookie=0x0, duration=3.991s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s2-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:05,nw_src=10.0.0.1,nw_dst=10.0.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s2-eth3"
cookie=0x0, duration=3.973s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s2-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.5,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s2-eth1"
```

In `s3`:
```
ovs-ofctl dump-flows s3
cookie=0x0, duration=4.020s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s3-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:05,nw_src=10.0.0.1,nw_dst=10.0.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s3-eth3"
cookie=0x0, duration=3.989s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s3-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.5,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s3-eth1"
```

In `s5`:
```
ovs-ofctl dump-flows s5
cookie=0x0, duration=5.222s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s5-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:05,nw_src=10.0.0.1,nw_dst=10.0.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s5-eth1"
cookie=0x0, duration=5.212s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s5-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.5,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s5-eth3"
```

In `s6`:
```
ovs-ofctl dump-flows s6
cookie=0x0, duration=2.271s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s6-eth3",vlan_tci=0x0000,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:05,nw_src=10.0.0.1,nw_dst=10.0.0.5,nw_tos=0,icmp_type=8,icmp_code=0 actions=output:"s6-eth1"
cookie=0x0, duration=2.269s, table=0, n_packets=1, n_bytes=98, idle_timeout=10, hard_timeout=30, priority=65535,icmp,in_port="s6-eth1",vlan_tci=0x0000,dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:01,nw_src=10.0.0.5,nw_dst=10.0.0.1,nw_tos=0,icmp_type=0,icmp_code=0 actions=output:"s6-eth3"
```

In `s4`:
```
ovs-ofctl dump-flows s4
```

In `s7`:
```
ovs-ofctl dump-flows s7
```

The rules in `s4` and `s7` are empty, which make sense because to send a message between `h1` and `h5`, it should only need to go through switches `s1`, `s2`, `s3`, `s5` and `s6`.

The rules that are defined in the related switches (`s1`, `s2`, `s3`, `s5` and `s6`) are similar to the ones we defined in part A. Let's take the rules in `s1` for instance. The first rule lets the switch forward the packet sent from source 10.0.0.1 (h1) which arrives from the "s1-eth1" interface to dest 10.0.0.5 (h2) via the "s1-eth2" interface. Unlike the rule we defined in part A, it also defined an idle_timeout and hard_timeout which will delete this flow entry after the specified interval. Moreover, it did not try to change the `src` and `dest` MAC addresses because the switches here are L2 switches instead of the L3 ones from part A. The flow entry also identified the type of message the switch receives as denoted by `icmp_type` and `icmp_code`: we see that the first rule (which lets the switch send out the ping) is an echo request (by type=8 and code=0), and the second rule (which lets h1 receive the reply) is an echo reply (by type=0 and code=0). The same goes with all other switches where the first rule letss the switch send out the message from `h1` to `h5`; and the second rule is there for the reverse direction.