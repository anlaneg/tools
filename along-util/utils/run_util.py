import os
import subprocess

class Run(object):
    @staticmethod
    def system(cmd):
        return os.system(cmd)

    @staticmethod
    def systems(cmds):
        for cmd in cmds:
            Run.system(cmd)

    @staticmethod
    def popen(cmd):
        return os.popen(cmd).readlines()

    @staticmethod
    def execl(cmd):
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.stdout,p.stderr,p

