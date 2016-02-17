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

import numpy as np

class DataPolishing:
    def __init__(self, Graph):
        self.Graph = Graph.simplify()   #グラフを単純グラフにする
        print "init Graph"

    def polish(self, vertex0, vertex1, sim, polish_ratio = 0.3):      #類似度を基に辺の取り外しを行う
        are_connected_flag = self.Graph.are_connected(vertex0, vertex1) ##vertex0とvertex1の間に辺があるか
        if(not(are_connected_flag) and sim[vertex0][vertex1] >= polish_ratio):    #辺がつながっていなくて類似度が大きい
            self.Graph.add_edge(vertex0, vertex1)
        elif(are_connected_flag and sim[vertex0][vertex1] < polish_ratio):        #辺がつながっていて類似度小さい
            self.Graph.delete_edges((vertex0,vertex1))

    def data_polish_direct(self, polish_ratio = 0.3, loop = 30):      #directな方法
        for i in xrange(loop):
            sim = self.Graph.similarity_jaccard()
            temp = self.Graph.get_edgelist()
            for j in xrange(self.Graph.vcount()):
                for k in [x for x in xrange(self.Graph.vcount()) if x < j]:
                    self.polish(j, k, sim, polish_ratio)
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
        print "end", i+1 , "times"

    def data_polish(self, polish_ratio = 0.3, loop = 30):       #グラフがスパースであれば高速
        for i in xrange(loop):
            sim = self.jaccard()
            temp = self.Graph.get_edgelist()
            for u in xrange(self.Graph.vcount()):
                for w in self.Graph.neighbors(u):
                    for v in [x for x in self.Graph.neighbors(w) if x < u]:
                        self.polish(u, v, sim, polish_ratio)
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
        print "end", i+1 , "times"

    def jaccard(self):                                          #グラフがスパースならば高速に類似度を計算
        sim = np.zeros([self.Graph.vcount(), self.Graph.vcount()])
        intersection = [0] * self.Graph.vcount()
        for u in xrange(self.Graph.vcount()):
            L = []
            for w in self.Graph.neighborhood(u):
                for v in [x for x in self.Graph.neighborhood(w) if x <= u]:
                    if(intersection[v] == 0):
                        L.append(v)
                    intersection[v] += 1
            for v in L:
                #print (v, u.index, intersection[v])
                sim[v][u] = float(intersection[v]) / (self.Graph.neighborhood_size(v)+ self.Graph.neighborhood_size(u) - intersection[v])
                sim[u][v] = sim[v][u]
                intersection[v] = 0
        return sim
