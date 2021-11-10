#! /usr/bin/env/ python3
from threading import Thread
import datetime
import pytz
from optparse import OptionParser
# from utilities.ssh.ssh2 import startSSH
import pyfiglet

def getTime():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
def startSSH():
    print("SSH should work")

def http():
    print("HTTP should work after threading")
parser = OptionParser(conflict_handler="resolve")


parser.add_option('-h',
                    dest = 'http', 
                    action = "store_true",
                    default = False,
                    help = 'To start HTTP honeypot')

parser.add_option("-s",
                    action = "store_true",
                    dest = "ssh",
                    default = False,
                    help = "To start SSH honeypot")
    
(options, args) = parser.parse_args()
print(pyfiglet.figlet_format('HoneyPot'))
print("\t\t\t\tby Vishnu\n\n")
if (options.ssh and options.http):
    raise Exception("Not possible to add both services at same time.")
elif options.ssh:
    sshThread = Thread(target = startSSH)
    sshThread.start()
    print(f'{getTime(): <25} : ssh')
elif options.http:
    httpThread = Thread(target = http)
    httpThread.start()
    print(f'{getTime(): <25} : http')