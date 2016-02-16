# -*- coding: utf-8 -*-
'''
Created on 2016/02/05

@author: gocho
'''

import igraph
from data_polishing import DataPolishing

pr = 0.3
#g = igraph.read("E:\\IT_Fundamental\\graphC.gml")
g = igraph.Graph.GRG(500, 0.1)     #ランダムグラフの作成。頂点を単位正方形上にランダムで配置する。引数(node数、dist)、頂点がdist以内なら辺をつなぐ
g2 = g.copy()
#print g
a = DataPolishing(g)
b = DataPolishing(g2)
igraph.summary(a.Graph)
print a.Graph.maximal_cliques(min = 3)
print len(a.Graph.maximal_cliques(min = 3))

#a.data_polish_direct(polish_ratio = pr)

b.data_polish(polish_ratio = pr)
#print a.Graph
#print a.Graph.maximal_cliques(min = 3)
#print len(a.Graph.maximal_cliques(min = 3))
print b.Graph.maximal_cliques(min = 3)
print len(b.Graph.maximal_cliques(min = 3))
#igraph.write(a.Graph, "polished_graph_direct.gml")
#igraph.write(b.Graph, "polished_graph.gml")

#igraph.summary(a.Graph)

igraph.summary(b.Graph)

