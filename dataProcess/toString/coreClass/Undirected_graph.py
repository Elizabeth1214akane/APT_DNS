## 定义数据处理无向图相关类
import sys


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
        self.degree = 0
        self.hostsIp = []

class Edge:

    def __init__(self,host,domain,times,timestamps):
        """
        一个beacon host-domain的查询 weight代表查询次数 timestamp时间戳
        :param host:
        :param domain:
        """
        self.host =  host
        self.domain = domain
        self.weight = times
        self.timestamps=[]
        self.timestamps.extend(timestamps)

class Graph:

    def __init__(self):
        self.hosts = []
        self.domains = []
        self.edges = []

    def addEdge(self,hostIP,domainName,times,timestamps):
        """
        构造相应的查询边
        :param hostIP:
        :param domainName:
        :param timestamp:
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
            domain.degree+=1
            domain.hostsIp.append(hostIP)
        elif hostIP not in domain.hosts:
            domain.degree+=1
            domain.hostsIp.append(hostIP)

        #开始构造边
        flag = False
        for edge in self.edges:
            if(edge.host.ip == host.ip and edge.domain.domainName == domain.domainName):
                edge.weight += times
                edge.timestamps.extend(timestamps)
                flag = True
                break

        #不存在该边
        if not flag:
            edge = Edge(host,domain,times,timestamps)
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
                hostIP = info[0]
                domainName = info[1]
                times = int(info[2])
                timestamps = line.split(' ')[3:]
                graph.addEdge(hostIP,domainName,times,timestamps)

        return graph

