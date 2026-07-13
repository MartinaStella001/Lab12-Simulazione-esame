import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._registi = []
        self._idMapRegisti = {}
        self._idMapIdRegisti = {}


    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, year):
        self._registi = DAO.getAllRegisti(year)
        for r in self._registi:
            self._idMapRegisti[r.id] = r
            self._idMapIdRegisti[r] = r.id
        self._grafo.add_nodes_from(self._registi)
        self.addEdges(year)

    def addEdges(self, year):
        self._edges = DAO.getAllEdges(year, self._idMapRegisti)
        for e in self._edges:
            peso = e.numFilmGenereComune*(e.regista1.ratingMedio + e.regista2.ratingMedio)
            self._grafo.add_edge(e.regista1, e.regista2, weight =peso)

    def getDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArtistaGradoMax(self):
        maxArista = None
        gradoMax = 0
        for n in self._grafo.nodes():
            grado = self._grafo.degree(n)
            if grado > gradoMax:
                maxArista = n
                gradoMax = grado
        return maxArista, gradoMax

    def getRegistaSommaPesiMax(self):
        listaRegistiPesi = []
        for n in self._grafo.nodes():
            #NON ORIENTATO
            sommaPesi = 0
            for v in self._grafo.neighbors(n):
                sommaPesi += self._grafo[v][n]["weight"]
            listaRegistiPesi.append((n,sommaPesi))
        listaRegistiPesi.sort(key=lambda x: x[1], reverse=True)
        return listaRegistiPesi[0]

    def best10archi(self):
        #NON orintati, se devo ordinare per NOME, prima
        listaOrdinata = []
        for u,v,data in self._grafo.edges(data=True):
            if u.name < v.name:
                listaOrdinata.append((u,v,data["weight"]))
            else:
                listaOrdinata.append((v,u,data["weight"]))
        listaOrdinata.sort(key=lambda x: (-x[2], x[0].name, x[1].name))
        return listaOrdinata[:10]
    #Premendo "Trova Collaborazione" si determini un cammino semplice tale che:
    # parta dal regista scelto
    # ogni regista successivo abbia rating medio minore o uguale al precedente
    # la lunghezza del cammino sia massimoù
    # Tra cammini di uguale lunghezza scegliere quello con somma pesi degli archi massima
    def getPath(self, source):
        self._bestPath = []
        self._bestCost = 0
        parziale =[source]
        self._ricorsione(parziale)
        return
    def _ricorsione(self, parziale):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
            self._bestCost = self._getTotPesi(parziale)
        elif len(parziale) == len(self._bestPath):
            if self._getTotPesi(parziale) > self._bestCost:
                self._bestPath = copy.deepcopy(parziale)
                self._bestCost = self._getTotPesi(parziale)
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale and n.ratingMedio <= parziale[-1].ratingMedio:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()
