import sys
from coreClass import Undirected_graph
from coreClass.Parameter import ParameterValue


def filter(graph,writePath):
    '''
    根据degree 和 weight 过滤beacon
    :param path:
    :return:
    '''

    edges = graph.edges

    with open(writePath,'a') as f:
        for edge in edges:
            if(edge.domain.degree <= 10 and edge.weight > ParameterValue.minWeight and edge.weight <ParameterValue.maxWeight):
                writeStr = edge.host.ip + ' ' + edge.domain.domainName + ' '+processTimestamps(edge.timestamps)+'\n'
                f.write(writeStr)

def processTimestamps(timestamps):
    '''
    处理时间戳函数
    :param timestamps:
    :return:
    '''
    timeStart = sys.maxsize  # 获取时间戳开始时间
    # 缩放
    timestamps = [int(float(i) * ParameterValue.scale) for i in timestamps]
    for timestamp in timestamps:
        if timestamp<timeStart:
            timeStart = timestamp
    timestamps = [i - timeStart for i in timestamps]
    timestamps = sorted(timestamps)
    #转化为时间间隔
    timestamps = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
    #转化为相应的字符串
    return ' '.join([str(i) for i in timestamps])