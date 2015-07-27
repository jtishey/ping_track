#!/usr/bin/env python
'''
ping_track_old.py
ping_track.py modified for python 2.6 compatibility
and no pyping support or root access.
 https://github.com/jtishey
'''

try:
   import time, datetime, sys, subprocess
except:
    print("Error with import")
    exit()

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
        process = subprocess.Popen("ping -c 1 -W 2 -q " + host + " | grep transmitted",
          shell=True,
          stdout=subprocess.PIPE,
          )
        result = process.communicate()[0].split('\n')
    except:      # If there's an error, print error msg and mark as down.
        time_log()
        print(str(ts) + " : " + str(host) + " - Error Connecting.")
        state = "DOWN"
        return state
    if str(result)[25] == "0":     # If the ping FAILS
        if state == "UP":          # and host was previously UP
            time_log()             # grab a timestamp and print message.
            print(str(ts) + " : " + str(host) + " is now down. (" + str(td) + ")")
            state = "DOWN"
    elif str(result)[25] == "1":   # If response recieved    # If the ping RESPONDS
        if state == "DOWN":        # and host was previously DOWN
            time_log()             # grab a timestamp and print message.
            print(str(ts) + " : " + str(host) + " is now up. (" + str(td) + ")")
            state = "UP"
    else:  # if something tragic happens, just leave.
        print("ERROR: Exiting...")
        print("Result = " + str(result))
        exit()
    return state

while True:   # Loop to send pings via call
    state = run_ping_check(state)
    time.sleep(3)   #  Currently 3 second interval on attempts.
