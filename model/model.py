import copy

import networkx as nx


from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapFilm = {}

        self._film = []

    def creaGrafo(self,voto):
        self._film = DAO.getAllFilm(voto)
        for f in self._film:
            self._idMapFilm[f.id] = f
            self._idMapIdFilm[f] = f.id
        self._grafo.add_nodes_from(self._film)
        self._addEdges(voto)

    def _addEdges(self,voto):
        self._edges = DAO.getAllEdges(voto, self._idMapFilm)
        for e in self._edges:
            film1 = e.film1
            film2 = e.film2
            peso = e.numAttoriComuni + e.numGeneriComune
            self._grafo.add_edge(film1,film2, weight=peso)
    def getDettagli(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def filmGradomax(self):

        maxGrado =0
        filmMax = None
        for n in self._grafo.nodes:
            grado = self._grafo.degree(n)
            if grado > maxGrado:
                maxGrado = grado
                filmMax = n
        return filmMax, maxGrado

    def filmPesoIncMax(self):
        listaFilmPesi = []
        for n in self._grafo.nodes:
            sommaPesi = 0

            for v in self._grafo.neighbors(n):
                sommaPesi += self._grafo[v][n]["weight"]

            listaFilmPesi.append((n,sommaPesi))
        listaFilmPesi.sort(key=lambda x: x[1], reverse=True)
        return listaFilmPesi[0]

    def best10archi(self):
        listaArchi = []
        for u,v, data in self._grafo.edges(data=True):
            listaArchi.append((u, v, data["weight"]))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        return listaArchi[:10]


    #Determinare ricorsivamente un cammino semplice che:
    # parta dal film selezionato
    # abbia rating non crescente
    # ogni nuovo film condivida almeno 2 attori con il precedente
    # Tra tutte le soluzioni ammissibili scegliere quella con:
    # massimo numero di film
    # In caso di parità:
    # massima somma dei rating


    def getPath(self, source):
        self._bestPath = []
        self._bestRating = 0
        parziale =[source]
        self._ricorsione(parziale)
        return self._bestPath

    def _ricorsione(self,parziale):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
            self._bestRating = self._getTotRating(parziale)

        elif len(parziale) == len(self._bestPath):
            if self._getTotRating(parziale) > self._bestRating:
                self._bestPath = copy.deepcopy(parziale)
                self._bestRating = self._getTotRating(parziale)


        for n in self._grafo.neighbors(parziale[-1]):
            if n.ratingMedio <= parziale[-1].ratingMedio and self._hasAttoriCom(n,parziale[-1]) and n not in parziale :
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def _hasAttoriCom(self,n, precedente):
        for e in self._edges:
            if e.film1 == n and e.film2 == precedente:
                attoriComune = e.numAttoriComuni
        if attoriComune >=2:
            return True
        return False

    def _getTotRating(self,parziale):
        totRating = 0
        for n in parziale:
            totRating += n.ratingMedio
        return totRating


