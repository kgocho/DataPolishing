# -*- coding: utf-8 -*-
'''
Created on 2016/02/10

@author: gocho
'''

import igraph
import time
from data_polishing import DataPolishing

pr = 0.3
g = igraph.Graph.GRG(500, 0.1)     #ランダムグラフの作成。頂点を単位正方形上にランダムで配置する。引数(node数、dist)、頂点がdist以内なら辺をつなぐ
#g = igraph.read("random_graph.gml")
g2 = g.copy()
a = DataPolishing(g)
b = DataPolishing(g2)

"""
igraph.summary(a.Graph)
#print a.Graph.maximal_cliques(min = 3)
#print len(a.Graph.maximal_cliques(min = 3))
start_time = time.clock()
a.data_polish_direct(polish_ratio = pr)
end_time = time.clock()
t1 = end_time - start_time
print "t1: ", t1
"""

igraph.summary(b.Graph)
print b.Graph.maximal_cliques(min = 3)
print len(b.Graph.maximal_cliques(min = 3))
start_time = time.clock()
b.data_polish(polish_ratio = pr)
end_time = time.clock()
t2 = end_time - start_time
print "t2: ", t2


#print a.Graph.maximal_cliques(min = 3)
#print len(a.Graph.maximal_cliques(min = 3))
print b.Graph.maximal_cliques(min = 3)
print len(b.Graph.maximal_cliques(min = 3))

#igraph.summary(a.Graph)
#igraph.write(a.Graph, "polished_random_graph_direct.gml")
igraph.summary(b.Graph)
#igraph.write(b.Graph, "polished_random_graph.gml")
