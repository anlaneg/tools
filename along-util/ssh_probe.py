#-*- coding: utf-8 -*-
#!/usr/bin/python 
import paramiko
import threading

def ssh2(ip,logins,cmd):
    for login in logins:
    	try:
        	ssh = paramiko.SSHClient()
        	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	ssh.connect(ip,22,login['username'],login['passwd'],timeout=5)
        	for m in cmd:
            		stdin, stdout, stderr = ssh.exec_command(m)
            		out = stdout.readlines()
            		#屏幕输出
            		for o in out:
                		print o,
        		print '%s\tOK,user:%s,passwd:%s\n'%(ip,login['username'],login['passwd'])
        	ssh.close()
                break
    	except:
                pass
        	#print '%s\tError\n'%(ip)


if __name__=='__main__':
    cmd = ['echo hello!']#你要执行的命令列表
    logins=[
          {'username':'root',
	     'passwd':'****'
          },

          {'username':'root',
	     'passwd':'*'
          },

          {'username':'root',
	     'passwd':'8'
          },

 	  {'username':'root',
	     'passwd':'root'
          },
    ]
    threads = []   #多线程
    print "Begin......"
    for i in range(1,254):
        ip = '10.100.17.'+str(i)
        a=threading.Thread(target=ssh2,args=(ip,logins,cmd))
        a.start() 


