import subprocess 
from time import sleep
from datetime import datetime

while(True):
	print('\n')
	print(datetime.now())
	subprocess.call("./google-domains-dynamic-dns-update.sh")
	sleep(300)
