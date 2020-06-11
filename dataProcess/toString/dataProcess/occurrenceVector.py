#产生
# class Edge:
#     pattern = ''   # 后缀树边上的字符串
#     current = []   # 出现向量

import dataProcess.suffixtree as suffix

#从构造的后缀树产生叶子节点的值（路径上的后缀在字符串的出现位置）
def leafValue(treeNode:suffix.Node,pattern,originString):
    if(treeNode.outedges == None):
        #该节点是叶子节点 该路径pattern的出现位置是 stringLength-pattern.length
        treeNode.ouccurenceVector.append(len(originString)-len(pattern))
    else:
        #非叶子节点
        for edge in treeNode.outedges.values():
            #后缀路径增加该边代表的路径
            newPattern = pattern + originString[edge[1] : edge[2]+1 if edge[2] != '#' else len(originString)]
            leafValue(edge[3],newPattern,originString)

#遍历叶子节点有值的后缀树 生成所有节点的发生向量
def travel(treeNode:suffix.Node):
    if (treeNode.outedges == None):#该节点是叶子节点 直接返回它的发生向量
        return treeNode.ouccurenceVector
    else:
        #非叶子节点获取它的所有边
        for edge in treeNode.outedges.values():
            treeNode.ouccurenceVector.extend(travel(edge[3]))
        return treeNode.ouccurenceVector

#遍历构造好发生向量的后缀树  得到边的集合
def getEdges(treeNode:suffix.Node,pattern,originString,edges):
    if treeNode.outedges != None:
        for edge in treeNode.outedges.values():
            #该边连接的不是叶子节点
            if(edge[3].outedges != None):
                #该边的模式
                newPattern = pattern + originString[edge[1]: edge[2] + 1 if edge[2] != '#' else len(originString)]
                #该边的发生向量
                ouccurenceVector = edge[3].ouccurenceVector
                #添加该边
                edges.append([newPattern,ouccurenceVector])
                getEdges(edge[3],newPattern,originString,edges)

#组合构造后缀树  得到叶子节点值  得到发生向量值  产生边集合
def Beacon2Tree2Edges(originString):
    tree, pst = suffix.build(originString + '$', regularize=True)
    leafValue(tree, '', originString)
    travel(tree)
    edges = []
    getEdges(tree, '',originString, edges)
    return edges

if __name__ == '__main__':
    docs = ['abcabbabb$']
    for text in docs:
        tree, pst = suffix.build(text, regularize=True)
    leafValue(tree, '', 'abcabbabb')
    travel(tree)
    edges=[]
    getEdges(tree, '',  'abcabbabb', edges)
    print(type(edges[0][1][1]))