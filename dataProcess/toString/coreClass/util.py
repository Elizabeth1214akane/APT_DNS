
class Tree :

    def __init__(self,lens,edges,host,domain,time2StrDict):
        self.lens = lens    # 字符串长度
        self.edges = edges  # 中间边的集合
        self.host = host    # 主机IP
        self.domain = domain #域名
        self.time2StrDict = time2StrDict #时间间隔和字符串的转化字典

class Edge:

    def __init__(self,pattern,current,value=0):
        self.pattern = pattern    # 后缀树边上的字符串
        self.current = current    #  出现向量
        self.value  = value      # 后缀树边对应的值


class Period:

    def __init__(self,pattern,val,stops,length,foundPosCount=-1,conf=0,avgVal=0,pattern_period =0):
        self.pattern = pattern # 周期字符
        self.val = val     # 周期长度
        self.stops = stops    # 当前所指的pattern的起始位置
        self.length = length   # pattern的长度
        self.foundPosCount = foundPosCount # 传说中的count,pattern在整个字符串中出现的字数
        self.conf = conf     # 周期性置信度
        self.avgVal = avgVal   # pattern 的平均周期
        self.pattern_period = pattern_period #pattern代表的间隔时间
