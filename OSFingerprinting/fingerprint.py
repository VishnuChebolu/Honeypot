# from scapy.all import sr
# from scapy.layers.inet import IP, ICMP

# packet = IP(dst="192.168.50.122")/ICMP()

# response = sr(packet, timeout=2)


# if response.getlayer(IP).ttl <=64:
#     print("linux os")
# else:
#     print("Windows")


import nmap

scanner = nmap.PortScanner()

ip = input("Enter an IP to perform OS fingerprinting attack : ")

a = scanner.scan(ip, arguments="-O")['scan'][ip]['osmatch']
# print(a)
print(a[0]['osclass'][0]['osfamily'])
