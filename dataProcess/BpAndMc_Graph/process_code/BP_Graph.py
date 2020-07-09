from scapy.all import *
import pickle
import scapy.all as scapy






def extract_information(filepath):
    packets = rdpcap(filepath)
    file = open(BP_information_path, "w")
    for packet in packets:  # 逐个报文
        try:
            DNS = packet["DNS"]  # 获取DNS层
            if DNS.haslayer("DNS Resource Record"):  # 获取response
                DRR = DNS["DNS Resource Record"]
                if DRR.type == 1:
                    # print(str(DRR.rrname, 'utf-8').rstrip('.'), DRR.rdata)
                    file.write(str(DRR.rrname, 'utf-8').rstrip('.') + ' ' + str(DRR.rdata) + '\n')
                while DRR.payload:
                    DRR = DRR.payload
                    if DRR.type == 1:
                        file.write(str(DRR.rrname, 'utf-8').rstrip('.') + ' ' + str(DRR.rdata) + '\n')
        except IndexError as e:
            print(e)
            packet.show()
    file.close()


class Host:

    def __init__(self,ip):
        """
        主机节点  源ip
        :param ip:
        """
        self.ip = ip



class Domain:

    def __init__(self,domainName):
        """
        域节点  包括域名 和 degree（多少不同host请求了） hostsIp 请求的主机列表
        :param domainName:
        """
        self.domainName = domainName


class Edge:

    def __init__(self,host,domain,times):
        """
        一个beacon host-domain的查询 weight代表查询次数
        :param host:
        :param domain:
        """
        self.host =host
        self.domain = domain
        self.weight = times


class Graph:

    def __init__(self):
        self.hosts = []
        self.domains = []
        self.edges = []

    def addEdge(self,hostIP,domainName,times):
        """
        构造相应的查询边
        :param hostIP:
        :param domainName:
        :return:
        """
        #查找是否有相应的host
        host = None
        for temp in self.hosts:
            if(temp.ip == hostIP):
                host = temp
                break
        if host == None:
            host = Host(hostIP)
            self.hosts.append(host)

        #查找是否有相应的domain:
        domain = None
        for temp in self.domains:
            if(temp.domainName == domainName):
                domain = temp
                break
        if domain == None:
            domain = Domain(domainName)
            self.domains.append(domain)

        #开始构造边
        flag = False
        for edge in self.edges:
            if(edge.host.ip == host.ip and edge.domain.domainName == domain.domainName):
                edge.weight += times
                flag = True
                break

        #不存在该边
        if not flag:
            edge = Edge(host,domain,times)
            self.edges.append(edge)

    @staticmethod
    def buildGraph(path):

        graph = Graph()
        with open(path) as f:
            for line in f:
                info = line.split(' ')
                domainName = info[0]
                hostIP = info[1][:-1]
                graph.addEdge(hostIP,domainName,1)

        return graph








if __name__ == "__main__":

    # 命名
    store_dir = 'F:\Myproject\APT_NEW_DATA\dataset'
    pcapfile_name = 'DNS.pcap'
    BP_information_name = 'BP_information.txt'
    # 命名

    BP_information_path = store_dir +'/' +BP_information_name
    # filepath = store_dir + '/' + pcapfile_name
    # extract_information(filepath)
    filepath = store_dir + '/' + BP_information_name
    graph = Graph.buildGraph(filepath)

    filepath = store_dir + '/' + "BPGraph.pkl"
    with open(filepath, 'wb') as writefile:
        pickle.dump(graph, writefile)