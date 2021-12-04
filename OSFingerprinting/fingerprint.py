# from scapy.all import sr
# from scapy.layers.inet import IP, ICMP

# packet = IP(dst="192.168.50.122")/ICMP()

# response = sr(packet, timeout=2)


# if response.getlayer(IP).ttl <=64:
#     print("linux os")
# else:
#     print("Windows")


import nmap
import datetime
import pytz
import sys


scanner = nmap.PortScanner()
def getOS(ip):
    a = scanner.scan(ip, arguments="-O")['scan'][ip]['osmatch']
    timenow = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
    print(f'[{timenow}] : Trying the fingerprint the OS of the client.')
    os = a[0]['osclass'][0]['osfamily']
    timenow = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %H:%M:%S")
    print(f'[{timenow}] : Detected {os} operating system.')
    return (a[0]['osclass'][0]['osfamily'])

getOS(sys.argv[1])