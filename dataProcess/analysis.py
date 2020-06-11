import  os

import scapy
from scapy.all import *

packets = rdpcap ("E:\dns_detection\dns_query.pcap")

edges = {}
count = 0

for p in packets:

  try:
    edge_dic = {'times': 0, 'time': []}
    if p.haslayer('IP') and p.haslayer('DNS'):
        print(type(p['DNS'].qd["DNSQR"].qname))
        hostAndDomain = "%s_%s" % (p['IP'].src,bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1])
        print(hostAndDomain)

        if p.haslayer('UDP') and p['UDP'].dport == 53 and p['UDP'].sport !=53:
                temp = edges.get(hostAndDomain)
                if temp!=None:
                    edges[hostAndDomain]['times'] = temp['times'] +1
                    edges[hostAndDomain]['time'].append(p.time)
                else:
                    edge_dic['host'] =p['IP'].src
                    edge_dic['domain'] = bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1]
                    edge_dic['times'] = edge_dic['times'] +1
                    edge_dic['time'].append(p.time)
                    edges[hostAndDomain] = edge_dic
        else :
                if p.haslayer('UDPerror') and p['UDPerror'].dport == 53 and p['UDPerror'].sport !=53:
                    temp = edges.get(hostAndDomain)
                    if temp != None:
                        edges[hostAndDomain]['times'] = temp['times'] + 1
                        edges[hostAndDomain]['time'].append(p.time)
                    else:
                        edge_dic['host'] = p['IP'].src
                        edge_dic['domain'] = bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1]
                        edge_dic['times'] = edge_dic['times'] + 1
                        edge_dic['time'].append(p.time)
                        edges[hostAndDomain] = edge_dic
  except Exception as e:
        print(e)
        s = repr(p)
        print(s)
        count= count +1


print(count)
count =0
f = open("E:\dns_detection\dns.txt",'w')
for value in edges.values():
    try:
      str1 = value['host']+' '+value['domain']+' '+str(value['times'])
      for time in value['time']:
          str1 = str1 +' '+ str(time)
      str1 = str1 + '\n'
      print(str1)
      f.write(str1)
    except Exception as e:
      print(e)
      count = count +1
print(count)