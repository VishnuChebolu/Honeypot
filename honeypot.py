#! /usr/bin/env/ python3
import datetime
import pytz
from optparse import OptionParser
from utilities.ssh.ssh2 import startSSH
from utilities.http.webserver import run
import pyfiglet

def getTime():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")


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
    startSSH()
elif options.http:
    run()