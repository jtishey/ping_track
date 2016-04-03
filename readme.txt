ping_track.py

Usage: sudo python ping_track.py <HOSTNAME/IP>

ping_track uses pyping library to send ICMP echo requests
to the host specified in the command argument.  Note that
it must be run as root because it is a requirement of pyping
for ICMP.  You can use UDP pings without root privelages by
specifying 'udp=True' after the host in the pyping.ping() call.
If run without the pyping lib installed, it will try an os call
to the ping command instead.  This does not requre root privileges.

H = pyping.ping(host, udp=True)


$ sudo python ping_track.py 10.0.10.4
2016-04-03_13:26:09 : 10.0.10.4 is now up. (0:00:02)
2016-04-03_13:27:32 : 10.0.10.4 is now down. (0:01:23)
2016-04-03_13:28:02 : 10.0.10.4 is now up. (0:00:30)

$ python ping_track_old.py 10.0.10.4
2016-04-03_13:29:47 : 10.0.10.4 is now up. (0:00:00)
2016-04-03_13:30:31 : 10.0.10.4 is now down. (0:00:44)
2016-04-03_13:30:49 : 10.0.10.4 is now up. (0:00:18)