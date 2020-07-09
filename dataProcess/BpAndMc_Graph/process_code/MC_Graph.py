from scapy.all import *
import pickle


def extract_information(filepath):
    edges = {}
    count = 0
    print(filepath)
    packets = rdpcap(filepath)
    for p in packets:
        try:
            edge_dic = {'times': 0}
            if p.haslayer('IP') and p.haslayer('DNS'):

                if p['DNS'].qr == 1:
                    continue  # 跳过响应报文
                # print(type(p['DNS'].qd["DNSQR"].qname))
                clientAndDomain = "%s_%s" % (p['IP'].src, bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1])
                # print(clientAndDomain)

                if p.haslayer('UDP') and p['UDP'].dport == 53 and p['UDP'].sport != 53:

                    temp = edges.get(clientAndDomain)
                    if temp != None:
                        edges[clientAndDomain]['times'] = temp['times'] + 1
                    else:
                        edge_dic['client'] = p['IP'].src
                        edge_dic['domain'] = bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1]
                        edge_dic['times'] = edge_dic['times'] + 1
                        edges[clientAndDomain] = edge_dic
                else:
                    if p.haslayer('UDPerror') and p['UDPerror'].dport == 53 and p['UDPerror'].sport != 53:
                        temp = edges.get(clientAndDomain)
                        if temp != None:
                            edges[clientAndDomain]['times'] = temp['times'] + 1
                        else:
                            edge_dic['client'] = p['IP'].src
                            edge_dic['domain'] = bytes.decode(p['DNS'].qd["DNSQR"].qname)[:-1]
                            edge_dic['times'] = edge_dic['times'] + 1
                            edges[clientAndDomain] = edge_dic
        except Exception as e:
            # print(e)
            # s = repr(p)
            # print(s)
            count = count + 1

    print(count)
    count = 0
    file_path = store_dir + '/' +MC_information_name # 这几个变量是全局的
    with open(file_path, 'w') as f:
        for value in edges.values():
            try:
                str1 = value['client'] + ' ' + value['domain'] + ' ' + str(value['times'])
                str1 = str1 + '\n'
                # print(str1)
                f.write(str1)
            except Exception as e:
                print(e)
                count = count + 1
        print(count)

class Client:

    def __init__(self,ip):
        """
        主机节点  源ip
        :param ip:
        """
        self.ip = ip



class Domain:

    def __init__(self,domainName):
        """
        域节点  包括域名 和 degree（多少不同client请求了） clientsIp 请求的主机列表
        :param domainName:
        """
        self.domainName = domainName
        self.degree = 0
        self.clientsIp = []

class Edge:

    def __init__(self,client,domain,times):
        """
        一个beacon client-domain的查询 weight代表查询次数
        :param client:
        :param domain:
        """
        self.client =client
        self.domain = domain
        self.weight = times


class Graph:

    def __init__(self):
        self.clients = []
        self.domains = []
        self.edges = []

    def addEdge(self,clientIP,domainName,times):
        """
        构造相应的查询边
        :param clientIP:
        :param domainName:
        :return:
        """
        #查找是否有相应的client
        client = None
        for temp in self.clients:
            if(temp.ip == clientIP):
                client = temp
                break
        if client == None:
            client = Client(clientIP)
            self.clients.append(client)

        #查找是否有相应的domain:
        domain = None
        for temp in self.domains:
            if(temp.domainName == domainName):
                domain = temp
                break
        if domain == None:
            domain = Domain(domainName)
            domain.degree+=1
            domain.clientsIp.append(clientIP)
            self.domains.append(domain)
        elif clientIP not in domain.clientsIp:
            domain.degree+=1
            domain.clientsIp.append(clientIP)
        else:
            domain.degree+=1

        #开始构造边
        flag = False
        for edge in self.edges:
            if(edge.client.ip == client.ip and edge.domain.domainName == domain.domainName):
                edge.weight += times
                flag = True
                break

        #不存在该边
        if not flag:
            edge = Edge(client,domain,times)
            self.edges.append(edge)

    @staticmethod
    def buildGraph(path):
        """
         [
          [10.59.13.204 android.clients.google.com 2 1562898034.163875 1562898034.19257]
          [10.59.13.204 android.clients.google.com 2 1562898034.163875 1562898034.19257]
        ]
        构建无向图
        :param data:
        :return:
        """
        graph = Graph()
        with open(path) as f:
            for line in f:
                info = line.split(' ')
                clientIP = info[0]
                domainName = info[1]
                times = int(info[2])
                graph.addEdge(clientIP,domainName,times)

        return graph

if __name__ == "__main__":

    # 命名
    store_dir = 'F:\Myproject\APT_NEW_DATA\dataset'
    pcapfile_name = 'DNS.pcap'
    MC_information_name = 'MC_information.txt'
    # 命名

    # filepath = store_dir + '/' + pcapfile_name
    # extract_information(filepath)

    filepath = store_dir + '/' +MC_information_name
    graph = Graph.buildGraph(filepath)

    filepath = store_dir + '/' + "MCGraph.pkl"
    with open(filepath,'wb') as writefile:
        pickle.dump(graph,writefile)

