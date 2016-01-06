# Contrail utilities
This repository stores contrail utilities
1) bumtreedisp.py
   This utility shows BMU tree on vRouter.
   use with vrouter IP address and VNI
   python bumtreedisp.py -t 172.27.113.207 -v 1802
   ### Host 172.27.113.207 VNI 1802 BUM Tree ###
   ---- TAP interfaces ----
   TAP:tap4c82d4c5-cc  MAC:02:4c:82:d4:c5:cc
   ---- Tunnel interfaces ----
   SIP:192.168.21.1    DIP:10.84.50.51     Encap:MPLSoUDP
   SIP:192.168.21.1    DIP:192.168.22.1    Encap:MPLSoGRE

