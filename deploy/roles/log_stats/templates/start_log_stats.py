#!/usr/bin/python3

import psutil
from subprocess import Popen

args = ["python3", "-m", "src.log_stats.log_stats"]

for process in psutil.process_iter():
    try:
        if process.cmdline() == args:
            print("log_stats Process found. Terminating it.")
            process.terminate()
            break
    except Exception as e:
        print("received error whilst looking at or terminating a process: {}".format(e))

print("start log_stats Process.")
nohup_args = ["nohup"] + args # + ["&"])  We needed to ampersand if invoking from command line
Popen(nohup_args, cwd="{{ REMOTE_MA_DIRECTORY }}")
