# Part B

(i) Brief description of topology:

We have the hosts `alice`, `bob` and `carol`, as well as routers `robert`, `richard` and `rupert`.

To simulate the BUS, we have an L2 switch connected btween `alice` and `robert`, an L2 switch connected between `robert`, `bob` and `richard`, and another L2 switch connected between `rupert`, `carol` and `richard`.

The IP addresses of the hosts and routers are set via `setIP` in the code. And the corresponding routing entries are also added via the `ip route add` commands in the script.


(ii) The OVS rules for switches in the topolgy.

The following are the ovs rules installed on the switches. Note that these rules will not only allow Alice ping Carol, it will also allow Bob ping Carol (and vice versas). 

On switch `s0`:
(Note the `#` are comments to make the commands clearer)
```
#[s0] if src is alice, route to robert
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=1,ip,nw_src=10.1.1.17 actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0B:01:00:03,output=2

#[s0] if dest is alice, route to alice
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=2,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1
```

On switch `s1`:
```
#[s1] only dest matters, route to the respective host or router. This one is for bob.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.4.4.48,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1

#[s1] only dest matters, route to the respective host or router. This one is for carol.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:02:01:00:01,output=3

#[s1] only dest matters, route to the respective host or router. This one is for alice.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:0A:FE:00:02,mod_dl_dst:0A:00:0C:01:00:03,output=2
``` 

On switch `s2`:
```
#[s2] only dest matters, route to the respective host or router. This one is for carol.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:03:02:00:00,output=1

#[s2] only dest matters, route to the respective host or router. This one is for alice.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:0D:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=2

#[s2] only dest matters, route to the respective host or router. This one is for bob.
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.4.4.48,actions=mod_dl_src:0A:00:0D:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=2
```