from utilities.ssh.ssh2 import startSSH
import cowsay
import pyfiglet
import time
import threading
cowsay.ghostbusters(pyfiglet.figlet_format('HoneyPot')+'\n\n\n  by vishnu')


startSSH()