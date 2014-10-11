arris-cmd
=========

Command line tools for configuring an Arris TG862 gateway.

This script is intended for the following (personal) use cases:

1. I occasionally want to modify my gateway settings remotely. Since the Arris TG862 uses HTTP requests for configuration, the only way to do this is to set up a full remote desktop environment or use lynx, both of which are a pain.
2. I want my computer to automatically configure the router to set up certain ports to forward to my desktop, without having to enable full DMZ access, and check on this periodically. The router doesn't always give my desktop the same local IP (even though I tell it to), for example when the network interface changes. 
3. I want to be able to save a settings profile in the event that a factory reset is needed. The Arris TG862 has a number of known issues--for example, the "connected devices" page can become broken, with the only fix being a factory reset.
