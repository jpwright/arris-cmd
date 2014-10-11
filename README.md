arris-cmd
=========

Command line tools for configuring an Arris TG862 gateway. This is designed for, and only tested on, an Ubuntu 14.04.1 machine.

This script is intended for the following (personal) use cases:

1. I occasionally want to modify my gateway settings remotely. Since the Arris TG862 uses HTTP requests for configuration, the only way to do this is to set up a full remote desktop environment or use lynx, both of which are a pain.
2. I want my computer to automatically configure the router to set up certain ports to forward to my desktop, without having to enable full DMZ access, and check on this periodically. The router doesn't always give my desktop the same local IP (even though I tell it to), for example when the network interface changes. 
3. I want to be able to save a settings profile in the event that a factory reset is needed. The Arris TG862 has a number of known issues--for example, the "connected devices" page can become broken, with the only fix being a factory reset.

How to use:

First, install dependencies (if you don't already have them) -- `pip install beautifulsoup4 mechanize`

Second, modify login.txt. Put your username (usually 'admin') on the first line, and password on the second.

Then run the script with one of the following options (more to come):

`arris.py devices` -- list devices currently connected. Note: This doesn't expose their local IPs just yet.  
`arris.py ports` -- show current port forwarding settings.  
`arris.py ports-update` -- update port forwarding settings to forward ports 22, 80, and 690 to the computer's local IP. These are the ports I happen to use, you'll need to modify the script a bit for your own purposes, eventually I will update this to use a settings file as well.  

*Important* -- When updating ports, the script will use the local IP of the computer running the script by checking eth0, eth1, and eth2 -- and using the IP of the first interface that works. If your network interfaces are called something different, or you don't want that behavior, you'll need to modify the script to suit your preferences.
