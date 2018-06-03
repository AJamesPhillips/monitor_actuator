#!/usr/bin/python3

import psutil
from subprocess import Popen

args = ["python3", "-m", "src.stat_reporter.stat_reporter"]

for process in psutil.process_iter():
    try:
        if process.cmdline() == args:
            print("stat_reporter Process found. Terminating it.")
            process.terminate()
            break
    except Exception as e:
        print("received error whilst looking at or terminating a process: {}".format(e))

print("start stat_reporter Process.")
nohup_args = ["nohup"] + args # + ["&"]  # We need to ampersand if invoking from command line
Popen(nohup_args, cwd="{{ REMOTE_MA_DIRECTORY }}")
