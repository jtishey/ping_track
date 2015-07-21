ping_track.py

Usage: sudo python ping_track.py <HOSTNAME/IP>

ping_track uses pyping library to send ICMP echo requests
to the host specified in the command argument.  Note that
it must be run as root because it is a requirement of pyping
for ICMP.  You can use UDP pings without root privelages by
specifying 'udp=True' after the host in the pyping.ping() call.
 
H = pyping.ping(host, udp=True)




