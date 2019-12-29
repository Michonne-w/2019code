#coding:utf-8
"""
新建一程序，对小说《黎明破晓的街道》分析并得到人物关系图
作者:温若澜
2019/12/26
"""

import jieba, codecs
import  jieba.posseg as pseg

name = {}   #建立人物姓名（即结点）的字典
relationship = {}   #人物关系(即连线）的字典
paranames = []  #每段中人物之间的关系

jieba.load_userdict('character.txt')    #加载已经写入主要人物的文件
file = codecs.open('黎明破晓的街道.txt', 'r', 'utf-8')
for x in file.readlines():
    seg = pseg.cut(x)   #对文章内容进行分词
    paranames.append([])
    for w in seg:
        if w.flag != 'nr' or len(w.word) < 2:   #判断词性，nr为人名
            continue
        paranames[-1].append(w.word)    #在当下的关系中添加一个人物
        if name.get(w.word) is None:
            name[w.word] = 0
            relationship[w.word] = {}
        name[w.word] += 1     #该人物每次出现时，次数加一
# for names,times in name.items():
#     if times>10:
#         print(names, times)
for l in paranames:
    for name1 in l:
        for name2 in l:
            if name1 == name2:
                continue
            if relationship[name1].get(name2) is None:
                relationship[name1][name2] = 1
            else:
                relationship[name1][name2] = relationship[name1][name2] + 1
                #为每段中出现的人物建立两两之间的关系线，出现次数越多权重越大

f = codecs.open('book_node.csv', 'w', 'gbk')
f.write('id, label, weight\r\n')
for names, times in name.items():
    if times > 20:  #筛选主要人物
        f.write(names + ',' + names + ',' + str(times) + '\r\n')  #将人物关系出现的次数写入结点文件中

f_1 = codecs.open('book_line.csv', 'w', 'gbk')
f_1.write('source, target, weight\r\n')
for names, lines in relationship.items():
    for v, w in lines.items():
        if w > 10:   #筛选掉关系出现次数少于等于10次的多余连线
            f_1.write(names + ',' + v + ',' + str(w) + '\r\n')

            #生成关于结点和连线的两个文档，用于gephi的可视化处理
file.close()
f.close()
f_1.close()
