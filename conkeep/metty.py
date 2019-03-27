#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import select
import termios
import tty
import pty
from subprocess import Popen

def setup_bash(command,remote_socket):
    #command = 'bash'
    # command = 'docker run -it --rm centos /bin/bash'.split()

    # save original tty setting then set it to raw mode
    old_tty = termios.tcgetattr(sys.stdin)
    #tty.setraw(sys.stdin.fileno())

    # open pseudo-terminal to interact with subprocess
    master_fd, slave_fd = pty.openpty()

    # use os.setsid() make it run in a new process group, or bash job control will not be enabled
    p = Popen(command,
          preexec_fn=os.setsid,
          stdin=slave_fd,
          stdout=slave_fd,
          stderr=slave_fd,
          universal_newlines=True)

    while p.poll() is None:
        r, w, e = select.select([remote_socket, master_fd], [], [])
        if remote_socket in r:
            d = os.read(remote_socket.fileno(), 10240)
            if d: 
                #print(d,'\n')
                #d="ls\n"
                os.write(master_fd, d)
        elif master_fd in r:
            o = os.read(master_fd, 10240)
            if o:
                os.write(remote_socket.fileno(), o)

    # restore tty settings back
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
