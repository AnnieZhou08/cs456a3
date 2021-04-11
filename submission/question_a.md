# Part A

(i) Explain what the flow entries that you entered do.

Take the first given command for instance:
```
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0A:FE:00:02, output=2
```
This command creates a flow entry (i.e. `add-flow`) such that the switch will listen on the tcp port at `127.0.0.1:6634` and for any IP traffic coming in at ingress port is 1, and the source has ip address `10.0.1.2`, then we modify the source MAC address to its own MAC address on interface 2 and the destination MAC address to switch 1's MAC address on interface 2 and forward the packet onto output link 2 (i.e. `s0-eth2`).

In other words, this command will allow `s0` to forward a packet from `h0` destined to `h1` to `s1`.

The other three commands are similar. 

- The second command will allow `s0` to forward a packet from `h1` sent via `s1` to `h0`. 
- The third command will allow `s1` to forward a packet from `h0` sent via `s0` to `h1`.
- The forth command will allow `s1` to forward a packet from `h1` destined to `h0` to `s0`.


(ii) Enabling communication between `h2 <-> h4` and `h1 <-> h6`:

For `h2 <-> h4`:
(insert the commands to the switch `_` in `s_ fwding msg...`; i.e. insert the first command below to `s2`)
```
# h2 -> h4
# s2 fwding msg from h2 (inlink = 1) to h4 (outlink = 4):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=1,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0D:01:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

# s3 fwding msg from h2 (inlink = 2) to h4 (outlink = 3):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:0E:FE:00:02,output=3

# s4 fwding msg from h2 (inlink = 2) to h4 (outlink = 1):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6638 in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:04:01:00:01,mod_dl_dst:0A:00:04:02:00:00,output=1

# h4 -> h2
# s4 fwding msg from h4 (inlink = 1) to h2 (outlink = 2)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6638 in_port=1,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:0E:FE:00:02,mod_dl_dst:0A:00:0E:01:00:03,output=2

# s3 fwding msg from h4 (inlink = 3) to h2 (outlink = 2)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=3,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0D:01:00:04,output=2

# s2 fwding msg from h4 (inlink = 4) to h2 (outlink = 1)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=4,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:02:01:00:01,mod_dl_dst:0A:00:02:02:00:00,output=1
```

For `h1 <-> h6`:
(similarly, insert commands to the switch `_` in `s_ fwding msg...`)
```
# h1 -> h6
# s1 fwding msg from h1 (inlink = 1) to h6 (outlink = 3):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0C:01:00:03,mod_dl_dst:0A:00:0C:FE:00:03,output=3

# s2 fwding msg from h1 (inlink = 3) to h6 (outlink = 4):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=3,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0D:01:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

# s3 fwding msg from h1 (inlink = 2) to h6 (outlink = 4):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0F:01:00:04,mod_dl_dst:0A:00:0F:FE:00:02,output=4

# s6 fwding msg from h1 (inlink = 2) to h6 (outlink = 1):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6640 in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:06:01:00:01,mod_dl_dst:0A:00:06:02:00:00,output=1

# h6 -> h1
# s6 fwding msg from h6 (inlink = 1) to h1 (outlink = 2):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6640 in_port=1,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0F:FE:00:02,mod_dl_dst:0A:00:0F:01:00:04,output=2

# s3 fwding msg from h6 (inlink = 4) to h1 (outlink = 2):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=4,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0D:01:00:04,output=2

# s2 fwding msg from h6 (inlink = 4) to h1 (outlink = 3):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=4,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0C:FE:00:03,mod_dl_dst:0A:00:0C:01:00:03,output=3

# s1 fwding msg from h1 (inlink = 3) to h6 (outlink = 1):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=3,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1
```

For `h0 <-> h3`:
(similarly, insert commands to the switch `_` in `s_ fwding msg...`)
```
# h0 -> h3:
# s0 fwding msg from h0 (inlink = 1) to h3 (outlink = 3):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:0B:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=3

# s2 fwding msg from h0 (inlink = 2) to h3 (outlink = 4):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:0D:01:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

# s3 fwding msg from h0 (inlink = 2) to h3 (outlink = 1):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:03:01:00:01,mod_dl_dst:0A:00:03:02:00:00,output=1

# h3 -> h0:
# s3 fwding msg from h3 (inlink = 1) to h0 (outlink = 2):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6637 in_port=1,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0D:01:00:04,output=2

# s2 fwding msg from h3 (inlink = 4) to h0 (outlink = 2):
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=4,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0B:FE:00:02,mod_dl_dst:0A:00:0B:01:00:03,output=2

# s0 fwding msg from h3 (inlink = 3) to h0 (outlink = 1)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=3,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1
```