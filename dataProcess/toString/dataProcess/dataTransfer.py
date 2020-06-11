
def dataToStr (path):
    threshold = 15 * 10**6
    with open( path,"r") as f :
        for line in f:
            info = line.strip("\n").split(" ")
            host = info[0]
            domain = info[1]
            intervals = info [2:]

            print(intervals)

            k=0         # 字符偏移值
            reflect = {}# 数字和字符的映射关系

            interval_init =[]
            for temp in intervals:
                interval_init.append(int(temp))
            # print(interval_init)

            # 排序进行单个数字和单个字符的映射
            temp_intrval = sorted(interval_init)
            # print(temp_intrval)
            i=0
            while(i<len(temp_intrval)):
                temp = temp_intrval[i]
                reflect[temp] = chr(97+k)
                if i == len(temp_intrval)-1:
                    break
                for j in range(i+1,len(temp_intrval)):
                    if 0<=int(temp_intrval[j]) - int(temp) <= threshold:
                        reflect[temp_intrval[j]] = chr(97+k)
                    else :
                        i = j
                        break
                    i=j
                k = k+1
            print(reflect)


            # 生成字符串
            chars = ''
            for interval in interval_init:
                chars = chars + reflect[interval]
            print(chars)

            str1 = ("%s %s %s")%(host,domain,chars)# 输出：host domain 字符串
            for i in intervals:             # 输出：时间间隔
                str1 = str1 +' ' + i
            for d in reflect.keys():           #输出：时间映射
                str1 = str1+ (' %d:%s')%(d,reflect[d])
            str1 = str1 + "\n"
            print(str1)


            f1 = open('E:\\dns_detection\\intervalToStr.txt',"a")
            f1.write(str1)
            f1.close()





dataToStr("E:\\dns_detection\\intervalResultdata.txt")


