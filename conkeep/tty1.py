 # encoding: utf-8
import os
import sys
import time


def child(master, slave):
    os.close(master)
    os.dup2(slave, 0)
    os.dup2(slave, 1)
    os.dup2(slave, 2)
    #os.execvp("/bin/bash", ["bash", "-l", "-i"])
    os.execvp("/bin/bash", ["bash", "-i"])


def parent(master,slave):
    new_pid = os.fork()
    if new_pid == 0:
        child(master, slave)

    time.sleep(1)
    os.close(slave)

    #os.write(master, "fg\n")
    #time.sleep(1)
    _ = os.read(master, 1024)
    print(_)

    os.write(master, sys.argv[1] + "\n")
    #time.sleep(1)
    lines = []
    while True:
        tmp = os.read(master, 1024)
        lines.append(tmp)
        if len(tmp) < 1024:
            break
    output = "".join(lines)
    output = "\n".join(output.splitlines()[1:])
    print output

if __name__ == "__main__":
    master, slave = os.openpty()
    parent(master,slave)
    while True:
        input = raw_input(">")#sys.stdin.read(1024)
        os.write(master,input)
        while True:
            tmp = os.read(master, 1024)
            #lines.append(tmp)
            print tmp
            if len(tmp) < 1024:
                break
