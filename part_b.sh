ovs-vsctl set bridge s2 protocols=OpenFlow13
ovs-ofctl dump-flows s2

#[s0] alice -> s0 -> {bob, carol} (only src matters, route to robert)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=1,ip,nw_src=10.1.1.17,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0B:01:00:03,output=2
#[s0] src -> s0 -> alice (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=2,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1


#[s1] src -> s1 -> bob (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.4.4.48,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1
#[s1] src -> s1 -> carol (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:02:01:00:01,output=3
#[s1] src -> s1 -> alice (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=*,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:0A:FE:00:02,mod_dl_dst:0A:00:0C:01:00:03,output=2


#[s2] src -> s2 -> carol (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:03:02:00:00,output=1
#[s2] src -> s2 -> alice (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:0D:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=2
#[s2] src -> s2 -> bob (only dest matters)
ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6636 in_port=*,ip,nw_dst=10.4.4.48,actions=mod_dl_src:0A:00:0D:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=2
