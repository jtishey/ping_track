#usr/bin/env python
'''
ping_track.py
 Requires root/administrator priviledges.
 Takes one arguemnt, which is a hostname/IP address.
 Example usage: ping_track.py google.com
 Sends an ICMP Echo Request once every ~3 seconds.
 Prints a timestamp and message when host goes up/down.
    https://github.com/jtishey/ping_track
'''
import pyping, time, datetime, sys

# Set initial timestamp, grab arg, and initalize connectivity status (state).
ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
host = str(sys.argv[1])
state = "DOWN"

def time_log():
    # Grabs last timestamp, makes a new one, and gives the difference.
    global ts, td
    ts_old = ts
    t = time.time()
    ts = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d_%H:%M:%S')
    x = time.mktime(time.strptime(ts,'%Y-%m-%d_%H:%M:%S'))
    y = time.mktime(time.strptime(ts_old,'%Y-%m-%d_%H:%M:%S'))
    td = datetime.timedelta(seconds=x-y)
    return

def run_ping_check(state):
    try:
        H = pyping.ping(host)
    except:             # If there's an error, print error msg and mark as down.
        time_log()
        print("{} : {} - Error Connecting.") .format(ts, host)
        state = "DOWN"
        return state
    if H.ret_code == 1:      # If the ping FAILS
        if state == "UP":    # and host was previously UP
            time_log()       # grab a timestamp and print message.
            print("{} : {} is now down. ({})") .format(ts, host, td)
            state = "DOWN"
    elif H.ret_code == 0:    # If the ping RESPONDS
        if state == "DOWN":  # and host was previously DOWN
            time_log()       # grab a timestamp and print message.
            print("{} : {} is now up. ({})") .format(ts, host, td)
            state = "UP"
    else:  # if something tragic happens, just leave.
        print("ERROR: Exiting...")
        exit()
    return state

while True:   # Loop to send pings
    state = run_ping_check(state)
    time.sleep(3)   #  Currently 3 second interval on attempts.
