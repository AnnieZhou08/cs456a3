# CS456 Assignment 3

## Environment setup

I am using a Macbook with the M1 chip, so I need a VM that can run on M1. The VM I installed is Parallels and I used an Ubuntu image.

Inside the VM, I installed mininet via Option 2 (Native Installation from Source: http://mininet.org/download/). I also `scp`'d the `topology.py` and other scripts into the `mininet` repo inside the VM.

To use `xterm`, I needed to install `XQuartz` and use the `XQuartz` terminal to ssh into my vm, i.e.
```
ssh anniezhou@10.211.55.3 -X
```
where `10.211.55.3` is the IP addr of my VM.

To run `mininet`, I need to use the `sudo -E ...` option, i.e.
```
sudo -E python topology.py
```
to use the xterm.

Afterwards I can just run `xterm` to access the terminal for each switch/node.
