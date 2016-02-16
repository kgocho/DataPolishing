# -*- coding: utf-8 -*-
'''
Created on 2016/02/05

@author: gocho
'''
"""
データ研磨の手法の実装
論文
"Micro-Clustering: Finding Small Clusters in Large Diversity, Takeaki Uno et.al"
"""

class DataPolishing:
    def __init__(self, Graph):
        self.Graph = Graph.simplify()   #グラフを単純グラフにする
        print "init Graph"

    def polish(self, vertex0, vertex1, sim, polish_ratio = 0.3):      #類似度を基に辺の取り外しを行う
        e = self.Graph.es.select(_within=[vertex0, vertex1])          #vertex0とvertex1の間の辺
        if(len(e) == 0 and sim[vertex0][vertex1] >= polish_ratio):    #辺がつながっていなくて類似度が大きい
            self.Graph.add_edge(vertex0, vertex1)
        elif(len(e) > 0 and sim[vertex0][vertex1] < polish_ratio):    #辺がつながっていて類似度小さい
            self.Graph.delete_edges((vertex0,vertex1))

    def data_polish_direct(self, polish_ratio = 0.3, loop = 30):      #directな方法
        for i in range(loop):
            sim = self.Graph.similarity_jaccard()
            temp = self.Graph.get_edgelist()
            for j in self.Graph.vs():
                for k in [x for x in self.Graph.vs() if x.index < j.index]:
                    self.polish(j.index, k.index, sim, polish_ratio)
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
        print "end", i+1 , "times"

    def data_polish(self, polish_ratio = 0.3, loop = 30):       #グラフがスパースであれば高速
        for i in range(loop):
            sim = self.Graph.similarity_jaccard()
            temp = self.Graph.get_edgelist()
            for u in self.Graph.vs():
                for w in self.Graph.neighbors(u):
                    for v in [x for x in self.Graph.neighbors(w) if x < u.index]:
                        self.polish(u.index, v, sim, polish_ratio)
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
        print "end", i+1 , "times"
