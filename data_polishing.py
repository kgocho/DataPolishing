# -*- coding: utf-8 -*-
'''
Created on 2016/02/05

@author: gocho
'''
from igraph.test.cliques import CliqueTests
from igraph.test import cliques
"""
データ研磨の手法の実装
論文
"Micro-Clustering: Finding Small Clusters in Large Diversity, Takeaki Uno et.al"
"""

import igraph
import numpy as np
from scipy.sparse import lil_matrix
import random
import time

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

    def polish_sparse(self, vertex0, vertex1, sim, polish_ratio = 0.3):      #類似度を基に辺の取り外しを行う
        are_connected_flag = self.Graph.are_connected(vertex0, vertex1) ##vertex0とvertex1の間に辺があるか
        if(not(are_connected_flag) and sim[vertex0, vertex1] >= polish_ratio):    #辺がつながっていなくて類似度が大きい
            self.Graph.add_edge(vertex0, vertex1)
        elif(are_connected_flag and sim[vertex0, vertex1] < polish_ratio):        #辺がつながっていて類似度小さい
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
            #starttime = time.clock()
            for u in xrange(self.Graph.vcount()):
                for w in self.Graph.neighbors(u):
                    for v in [x for x in self.Graph.neighbors(w) if x < u]:
                        self.polish(u, v, sim, polish_ratio)
            #endtime = time.clock()
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
            #print "maximal clique : ", len(self.Graph.maximal_cliques(min = 3))
            #print "time : " , endtime - starttime
        print "end", i+1 , "times"

    def data_polish_sparse(self, polish_ratio = 0.3, loop = 30):       #グラフがスパースであれば高速
        for i in xrange(loop):
            sim = self.jaccard_sparse()
            temp = self.Graph.get_edgelist()
            #starttime = time.clock()
            for u in xrange(self.Graph.vcount()):
                for w in self.Graph.neighbors(u):
                    for v in [x for x in self.Graph.neighbors(w) if x < u]:
                        self.polish_sparse(u, v, sim, polish_ratio)
            #endtime = time.clock()
            if(temp == self.Graph.get_edgelist()):
                print "break at " + str(i+1) + " times"
                break
            #igraph.summary(self.Graph)
            #print "maximal clique : ", len(self.Graph.maximal_cliques(min = 3))
            #print "time : " , endtime - starttime
        print "end", i+1 , "times"


    def jaccard(self):
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

    def jaccard_sparse(self):
        sim = lil_matrix((self.Graph.vcount(), self.Graph.vcount()))
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
                sim[v, u] = float(intersection[v]) / (self.Graph.neighborhood_size(v)+ self.Graph.neighborhood_size(u) - intersection[v])
                sim[u, v] = sim[v, u]
                intersection[v] = 0
        return sim

class Experiment():
    def __init__(self, *args, **kwds):          #初期化。python-igraphのグラフ初期化をそのまま利用
        self.Graph = igraph.Graph(*args, **kwds)
        self.clique_list = []

    def make_clique(self, clique_size, multiplicity = 1):
        if(self.Graph.vcount() < clique_size):
            print "Error. Clique size must be less than Graph size"
        else:
            clique_list = random.sample(xrange(self.Graph.vcount()), clique_size)
            self.clique_list.append(clique_list)
            edge_list = [(i, j) for i in clique_list for j in [x for x in clique_list if x < i]]
            self.Graph.add_edges(edge_list)

    def make_Graph(self, clique_size, clique_num, multiplicity = 1, prob = 0.0):
        for i in xrange(clique_num):
            self.make_clique(clique_size)
            self.Graph.simplify()
            self.Graph.rewire_edges(prob)

    def recall(self, Graph):
        p = []
        for i in self.clique_list:
            k = 0
            for j in Graph.maximal_cliques(min = 3):
                if k < len(set(i) & set(j)):
                    k = len(set(i) & set(j))
            p.append(float(k) / len(set(i)))
        return sum(p) / len(p)

    def precision(self, Graph):
        p = []
        for i in Graph.maximal_cliques(min = 3):
            k = 0
            for j in self.clique_list:
                if k < len(set(i) & set(j)):
                    k = len(set(i) & set(j))
            p.append(float(k) / len(set(i)))
        return sum(p) / len(p)

    def accuracy(self, Graph):
        p = self.precision(Graph)
        r = self.recall(Graph)
        return 2*p*r / (p+r)
