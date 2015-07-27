#!/usr/bin/env python
'''
ping_track.py
 Requires root privileges when using pyping library.
 If pyping imports without root, you'll get Errors.
 If no pyping, it'll use the os to ping (no root reqired).
 Takes one arguemnt, which is a hostname/IP address.
 Example usage: ping_track.py google.com
 Sends an ICMP Echo Request once every ~3 seconds.
 Prints a timestamp and message when host goes up/down.
    https://github.com/jtishey/ping_track
'''
import time, datetime, sys
try:
    import pyping
    ping_lib = True
except:
    import subprocess
    ping_lib = False

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

def run_pyping_check(state):
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

def run_ping_check(state):
    try:
        process = subprocess.Popen("ping -c 1 -W 2 -q " + host + " | grep transmitted",
          shell=True,
          stdout=subprocess.PIPE,
          )
        result = process.communicate()[0].split('\n')
    except:      # If there's an error, print error msg and mark as down.
        time_log()
        print("{} : {} - Error Connecting.") .format(ts, host)
        state = "DOWN"
        return state
    if str(result)[25] == "0":     # If the ping FAILS
        if state == "UP":          # and host was previously UP
            time_log()             # grab a timestamp and print message.
            print("{} : {} is now down. ({})") .format(ts, host, td)
            state = "DOWN"
    elif str(result)[25] == "1":   # If response recieved    # If the ping RESPONDS
        if state == "DOWN":        # and host was previously DOWN
            time_log()             # grab a timestamp and print message.
            print("{} : {} is now up. ({})") .format(ts, host, td)
            state = "UP"
    else:  # if something tragic happens, just leave.
        print("ERROR: Exiting...")
        print("Result = " + str(result))
        exit()
    return state

if ping_lib == True:
    while True:   # Loop to send pings via pyping
        state = run_pyping_check(state)
        time.sleep(3)   #  Currently 3 second interval on attempts.
elif ping_lib == False:
    while True:   # Loop to send pings via call
        state = run_ping_check(state)
        time.sleep(3)   #  Currently 3 second interval on attempts.
else:
    print("Error with library import state.")
