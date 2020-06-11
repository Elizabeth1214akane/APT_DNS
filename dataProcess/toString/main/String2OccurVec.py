#读入字符串文件并产生边集合文件
import os
import coreClass.util as util
import pickle
import dataProcess.occurrenceVector as occurrenceVector

if __name__ == '__main__':
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir,'processedData','intervalToStr.txt')) as fread:
        with open(os.path.join(baseDir,'processedData','edges.txt'),'a') as fwrite:
            with open(os.path.join(baseDir, 'processedData', 'Trees.pkl'), 'wb') as Objwrite:
                Trees = []
                for line in fread:
                    info = line.split(' ')
                    host = info[0]
                    domain = info[1]
                    originString = info[2]
                    time2StrDict = {}
                    dictFirstIndex = -1
                    for i,j in enumerate(info):
                        if ':' in j:
                            dictFirstIndex = i
                            break
                    for item in info[dictFirstIndex :]:
                        symbol = item.split(':')[1]
                        if '\n' in symbol:
                            symbol = symbol[:-1]
                        value = item.split(':')[0]
                        if time2StrDict.get(symbol) == None:
                            time2StrDict[symbol] = value
                        elif int(value) < int(time2StrDict[symbol]):
                            time2StrDict[symbol] = value
                    edges = occurrenceVector.Beacon2Tree2Edges(originString)
                    edgeObjects = []
                    for edge in edges:
                        edgeObjects.append(util.Edge(edge[0],sorted(edge[1])))
                    Tree = util.Tree(len(originString),edgeObjects,host,domain,time2StrDict)
                    Trees.append(Tree)
                    writeStr = host+" "+domain+" "+"strLength:"+str(len(originString))+" "+"dict:"+" "
                    for item in time2StrDict.items():
                        writeStr+=item[0]+":"+item[1]+" "
                    writeStr+="edges:"+" "
                    for edge in edges:
                        writeStr+=edge[0]+":"+'_'.join([str(i) for i in edge[1]])+" "
                    writeStr = writeStr[:-1]+'\n'
                    fwrite.write(writeStr)
                pickle.dump(Trees,Objwrite)