import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._attori = []
        self._idMapAttori = {}
        self._bestPath = []
        self._bestCost = 0


    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def creaGrafo(self,genere):
        self._grafo.clear()
        self._attori = DAO.getAllAttori(genere)
        for a in self._attori:
            self._idMapAttori[a.id] = a
        self._grafo.add_nodes_from(self._attori)
        self.addEdges(genere)

    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def addEdges(self, genere):
        self._edges = DAO.getAllEdges(genere, self._idMapAttori)
        for e in self._edges:
            attore1 = e.attore1
            attore2 = e.attore2
            peso = e.numFilmComune *(abs(attore1.ratingMedio - attore2.ratingMedio))
            if attore1.ratingMedio > attore2.ratingMedio:
                    self._grafo.add_edge(attore1, attore2, weight=peso)
            elif attore2.ratingMedio == attore1.ratingMedio:
                    self._grafo.add_edge(attore1, attore2, weight=peso)
                    self._grafo.add_edge(attore2, attore1, weight=peso)
            else:
                    self._grafo.add_edge(attore2, attore1, weight=peso)


    def getAttorePiuInfluente(self):

        listaAttoriInflu = []
        for n in self._grafo.nodes:
            sommaPesiEntranti = 0
            sommaPesiUscenti = 0
            predecessors = self._grafo.predecessors(n)
            #ATTENZIONE AI VERSI
            for p in predecessors:
                sommaPesiEntranti += self._grafo[p][n]["weight"]
            successors = self._grafo.successors(n)
            for s in successors:
                sommaPesiUscenti += self._grafo[n][s]["weight"]

            listaAttoriInflu.append((n, (sommaPesiUscenti - sommaPesiEntranti)))
        listaAttoriInflu.sort(key=lambda x: x[1], reverse=True)
        return listaAttoriInflu[0]

    def get10Attori(self):
        listaAttori = []
        for n in self._grafo.nodes:
            out_degreeN = self._grafo.out_degree(n)
            listaAttori.append((n, out_degreeN))
        listaAttori.sort(key=lambda x: x[1], reverse=True)
        return listaAttori[:10]
    def getAllAttori(self):
        return self._attori

    #Determinare ricorsivamente un insieme di attori tale che:
    # contenga esattamente N attori
    # il primo sia quello scelto
    # ogni nuovo attore sia adiacente ad almeno uno già presente
    # nessuna coppia di attori abbia recitato insieme in più di 5 film
    # Tra tutte le soluzioni ammissibili scegliere quella che massimizza:somma rating medio

    def getPath(self, source,N):
        self._bestPath =[]
        self._bestCost = 0
        parziale = [source]
        self._ricorsione(parziale,N)
        return self._bestPath, self._bestCost

    def _ricorsione(self,parziale,N):
        if len(parziale) == N:
            totRating = self._getTotRating(parziale)
            if totRating > self._bestCost:
                self._bestCost = totRating
                self._bestPath = copy.deepcopy(parziale)

            return

        for candidato in self._grafo.nodes:
            if self.hasArco(parziale, candidato) and not self.hasPesoMax5(parziale, candidato) and candidato not in parziale:
                parziale.append(candidato)
                self._ricorsione(parziale,N)
                parziale.pop()

    def hasArco(self,parziale,candidato):

        for n in parziale:
            if self._grafo.has_edge(n,candidato) or self._grafo.has_edge(candidato,n):
                return True
        return False

    def hasPesoMax5(self,parziale,candidato):

        for n in parziale:
            if self._grafo.has_edge(n,candidato):
                if self._grafo[n][candidato]["weight"] > 5 :
                    return True
            if self._grafo.has_edge(candidato,n):
                if self._grafo[candidato][n]["weight"] > 5 :
                    return True
        return False

    def _getTotRating(self,parziale):
        totRating = 0
        for n in parziale:
            totRating += n.ratingMedio
        return totRating