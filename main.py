import numpy as np
import math
import heapq
import sys

WHITE = 0
GREY = 1
BLACK = 2

class Graph:
    bool_dfs = False
    adj_list = []
    adj_list_T = []
    scc_list = []
    num_vertex = 0
    widths = []
    nomen = []
    
    def __init__(self, filename, directed = True):
        with open(filename) as file:
            rows = file.readlines()
            
            
            aux = rows[0].split(' ')
            
            self.num_vertex = int(aux[0])
            
            self.adj_list = [[] for _ in range(self.num_vertex)]
            self.adj_list_T = [[] for _ in range(self.num_vertex)]
            
            
            self.widths = np.zeros((self.num_vertex, self.num_vertex), dtype=np.int64)
            self.nomen = [[""]*self.num_vertex for _ in range(self.num_vertex)]
        
            
            rows.pop(0)
            
            for i in rows:
                i = i.split(' ')
                a     = int(i[0])
                b     = int(i[1])
                width = int(i[2])
                
                self.adj_list[a].append(b)
                if not directed: self.adj_list[b].append(a)
                
                self.widths[a][b] = width
                if not directed: self.widths[b][a] = width
                
                self.adj_list_T[b].append(a)
        
    def dfs_visit(self, u, adj_list = None, lst_aux = []):
        if not adj_list: 
            adj_list = self.adj_list
            
        self.colors[u] = GREY
        self.mark = self.mark+1
        self.d[u] = self.mark
        
        lst_aux.append(u)
        for v in adj_list[u]:
            if self.colors[v] == WHITE:
                self.dfs_visit(v, adj_list, lst_aux)
                self.nomen[u][v] = "Arvore"
            elif self.colors[u] == GREY and self.colors[v] == GREY:
                self.nomen[u][v] = "Retorno"
            elif self.colors[v] == BLACK:
                if self.d[u] < self.f[v]:
                    self.nomen[u][v] = "Avanço"
                else:
                    self.nomen[u][v] = "Cruzamento"
        
        
        self.ord_top.append(u)
        self.colors[u] = BLACK
        self.mark = self.mark+1
        self.f[u] = self.mark
        
        
        
    def dfs(self, v = 0):
        self.bool_dfs = True
        self.colors = [WHITE]*self.num_vertex
        self.d = [0]*self.num_vertex
        self.f = [0]*self.num_vertex
        self.ord_top = []
        
        self.mark = 0
        
        V = [v]
        
        for u in range(0, self.num_vertex):
            if u != v: V.append(u)
        
        for u in V:
            if self.colors[u] == WHITE:
                self.dfs_visit(u)        
        
        
                
        print('Tempo Inicial  : ', self.d)
        print('Tempo Final    : ', self.f)
        print('Ord Topologica : ', self.ord_top)
        print('')
    
    def dfs_scc(self, v):
        self.colors = [WHITE]*self.num_vertex
        self.d = [0]*self.num_vertex
        self.f = [0]*self.num_vertex
        
        self.mark = 0
       
        V = [v]
        
        for u in range(0, self.num_vertex):
            if u != v: V.append(u)

        for u in V:
            lst_aux = []
            if self.colors[u] == WHITE:
                self.dfs_visit(u, self.adj_list_T, lst_aux)
                self.scc_list.append(lst_aux)        
                
        
        print('Tempo Inicial: ', self.d)
        print('Tempo Final  : ', self.f)
        print('')
    
    def maior_f(self):
        maior = 0

        for i in range(0, len(self.f)):
            if self.f[i] > self.f[maior]:
                maior = i

        return maior

    def scc(self, v=0):
        self.dfs(v)

        maiorf = self.maior_f()
        print(self.f, maiorf)
        self.dfs_scc(maiorf)
        
        print(self.scc_list )
        
    def bfs(self, s):
        colors = []
        d = []
        pi = []
        
        for _ in range(0, self.num_vertex):
            colors.append(WHITE)
            d.append(math.inf)
            pi.append(None)
        
        colors[s] = GREY
        d[s] = 0
        
        Q = [s]
        
        while Q:
            u = Q.pop()
            
            for vert in self.adj_list[u]:
                if colors[vert] == WHITE:
                    colors[vert] = GREY
                    pi[vert] = u
                    d[vert] = d[u] + 1
                    Q.append(vert)

            colors[vert] = BLACK
            
        print('Tempo Inicial: ', d)
        print('Predecessores: ', pi)
        print('')
        
    def dijkstra(self, s):
        d = []
        pi = []
        
        for i in range(0, self.num_vertex):
            d.append(sys.maxsize)
            pi.append(None)
        
        d[s] = 0
        Q = []
        
        heapq.heapify(Q)
        
        heapq.heappush(Q,(s,0))
        
        while Q: 
            [u,pd] = heapq.heappop(Q)
            
            for v in self.adj_list[u]:
                if d[v] > d[u] + self.widths[u][v]:
                    d[v] = d[u] + self.widths[u][v]
                    pi[v] = u
                    heapq.heappush(Q,(v,d[v]))
            
        print('Distancias : ', d)
        print('Pi         : ', pi)
        print('')

    def nomenclature(self):
        if not self.bool_dfs:
            print('Dfs ainda nao executado!')
            return

        
        for i in range(self.num_vertex):
            for j in range(self.num_vertex):
                if self.nomen[i][j]:
                    print(f'Aresta {i} --> {j}: {self.nomen[i][j]}')
    
    def edges2array(self):
        edges = []
        for i in range(0, self.num_vertex):
            for u in self.adj_list[i]:
                if (i, u) not in edges and (u, i) not in edges:
                    edges.append((i, u))

        return edges

    def bellman_ford(self, s = 0):
        d = []
        pi = []
        
        for i in range(0, self.num_vertex):
            d.append(math.inf)
            pi.append(None)
        
        d[s] = 0

        edges = self.edges2array()

        for i in range(1, self.num_vertex):
            for (u, v) in edges:
                if d[v] > d[u] + self.widths[u][v]:
                    d[v] = d[u] + self.widths[u][v]
                    pi[v] = u

        print('Dist : ', d)
        print('PI   : ', pi)

    def inTuple(self, v, tuple):
        for (a, _) in tuple:
            if a == v: return True
        
        return False


    def heap_top(self, heap, chave):
        aux = heap[0]

        for i in heap:
            if chave[i] < chave[aux]:
                aux = i
        
        return aux

    def prim(self, s = 0):
        chave = []
        pi = []
        
        for i in range(0, self.num_vertex):
            chave.append(math.inf)
            pi.append(None)
        
        chave[s] = 0

        Q = []

        for i in range(0, self.num_vertex):
            Q.append(i)
        
        while Q: 
            u = self.heap_top(Q, chave)
            Q.remove(u)
            
            for v in self.adj_list[u]:
                
                if v in Q and chave[v] > self.widths[u][v]:
                    chave[v] = self.widths[u][v]
                    pi[v] = u

        T = []
        peso_agm = 0

        for i in range(0, len(pi)):
            if i != s:
                T.append((i, pi[i]))
                peso_agm= peso_agm + self.widths[i][pi[i]]

        print('Dist        : ', chave)
        print('PI          : ', pi)
        print('Arvore      : ', T)
        print('Peso da AGM : ', peso_agm)

    def makeset(self, u):
        self.pi[u] = u
        self.rank[u] = 0

    def find(self, x):
        while x != self.pi[x]:
            x = self.pi[x]
        
        return x
        
    def union(self, u, v):
        pu = self.find(u)
        pv = self.find(v)
        if self.rank[pu] > self.rank[pv]:
            self.pi[pv] = pu
        else:
            self.pi[pu] = pv
            if self.rank[pu] == self.rank[pv]:
                self.rank[pv] = self.rank[pv] + 1

    def order_edges(self):
        edges = self.edges2array()
        i = len(edges)
        sorted = False
        while i > 1 and not sorted:
            sorted = True
            
            for j in range (1, i):
                (a,b) = edges[j-1]
                key = self.widths[a][b]
                (a,b) = edges[j]

                key_2 = self.widths[a][b]

                if key > key_2:
                    temp = edges[j-1]
                    edges[j-1] = edges[j]
                    edges[j] = temp
                    sorted = False

        return edges
                
    def kruskal(self, w=0):
        self.pi = []
        self.rank = []
        for i in range(0, self.num_vertex):
            self.pi.append(i)
            self.rank.append(0)
        T = []
        edges = self.order_edges()

        agm = 0
        for (u, v) in edges:
            if self.find(u) != self.find(v):
                T.append((u, v))
                agm = agm + self.widths[u][v]
                self.union(u,v)

        print('Pi        : ', self.pi)
        print('Rank      : ', self.rank)
        print('Arvore    : ', T)
        print('AGM weight : ', agm)

n = Graph('grafos/prim-kruskal.txt', directed=False)

n.kruskal()

