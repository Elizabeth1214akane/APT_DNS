##读入数据并产生时间间隔序列
import os
from coreClass.Undirected_graph import Graph
from dataProcess import BeaconFilter

if __name__ == '__main__':
    graph = Graph.buildGraph(os.path.join(os.path.dirname(os.getcwd()),'processedData','dns.txt'))
    BeaconFilter.filter(graph,os.path.join(os.path.dirname(os.getcwd()),'processedData','intervalResultdata.txt'))
