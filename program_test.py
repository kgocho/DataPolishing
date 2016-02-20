# -*- coding: utf-8 -*-
'''
Created on 2016/02/05

@author: gocho
'''

import igraph
from data_polishing import DataPolishing
from data_polishing import Experiment

pr = 0.35
#g = igraph.read("E:\\IT_Fundamental\\graphC.gml")
#g = igraph.read("randam_test.gml")
#g = igraph.Graph.GRG(5000, 0.02)     #ランダムグラフの作成。頂点を単位正方形上にランダムで配置する。引数(node数、dist)、頂点がdist以内なら辺をつなぐ
#igraph.write(g, "randam_test.gml")
#a = DataPolishing(g)
#igraph.summary(a.Graph)
#print a.Graph.maximal_cliques(min = 3)
#print len(a.Graph.maximal_cliques(min = 3))

#a.data_polish(polish_ratio = pr)

#print a.Graph.maximal_cliques(min = 3)
#print len(a.Graph.maximal_cliques(min = 3))
#igraph.write(a.Graph, "polished_grapht.gml")
#igraph.summary(a.Graph)

c = Experiment(5000)

igraph.summary(c.Graph)
c.make_Graph(30,100)
igraph.summary(c.Graph)
#print len(c.clique_list)
g = c.Graph.copy()
d = DataPolishing(g)
igraph.summary(d.Graph)
print len(d.Graph.maximal_cliques(min = 3))
#igraph.write(d.Graph, "randam_clique_5000.gml")
d.data_polish(polish_ratio = pr)
igraph.summary(d.Graph)
print len(d.Graph.maximal_cliques(min = 3))
#igraph.write(d.Graph, "polished_clique_5000.gml")
print "recall = " , c.recall(d.Graph)
print "precision = " , c.precision(d.Graph)
print "accuracy = " , c.accuracy(d.Graph)
