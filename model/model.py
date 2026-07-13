import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapAttori= {}
        self._idMapAttori2 = {}
        self._bestPath = []


        self._grafo2 = nx.Graph()
        self._grafo3 = nx.DiGraph()
        self._grafo5 = nx.DiGraph()
        self._grafo10 = nx.Graph()

    def getAllRatings(self):
        return DAO.getAllRatings()

    def creaGrafo(self, voto1, voto2):
        self._grafo.clear()
        self._attori = DAO.getAllNodes(voto1,voto2)
        for a in self._attori:
            self._idMapAttori[a.id]= a
        self._grafo.add_nodes_from(self._attori)
        self.addEdges(voto1, voto2)

    def addEdges(self, voto1, voto2):
        self._edges = DAO.getAllEdges(self._idMapAttori, voto1, voto2)
        for e in self._edges:
            self._grafo.add_edge(e.attore1, e.attore2, weight =e.incasso)


    def best5Archi(self):
        bestArchiTuple = []
        for e in self._edges:
            bestArchiTuple.append((e.attore1, e.attore2, e.incasso))
        bestArchiTuple.sort(key= lambda x:x[2] , reverse=True)
        return bestArchiTuple[:5]

    def getCompConnesse(self):
        componenti = list(nx.connected_components(self._grafo))
        bestComp = sorted(componenti, key= lambda x:len(x), reverse=True)
        bestComp2 = max(componenti, key= len)
        return len(componenti),bestComp[0]

    def getDettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getPath(self):
        self._bestPath = []

        parziale = []
        #PARTI DA OGNI NODO... NON SPECIFICA UNO DI PARTENZA
        for n in self._grafo.nodes:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath

    def _ricorsione(self, parziale):

        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            #SEMPLICE E CON ETA DESC
            if n.date_of_birth < parziale[-1].date_of_birth and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()


        #VERSIONE 2
        # a) L'utente seleziona un anno di nascita.
        # b)Premendo "Crea Grafo" si costruisce un grafo non orientato e pesato.
        # Vertici: attori nati dopo l'anno selezionato.
        # Arco: due attori sono collegati se hanno recitato nello stesso film.
        # Peso: numero di film recitati insieme.
        # c)Visualizzare:numero vertici, numero archi, grado medio del grafo, attore con grado massimo, elenco dei 10 archi con peso maggiore
        # PUNTO 2
        # a)Trovare la componente connessa più numerosa.
        # b)Ricorsivamente trovare un cammino semplice di lunghezza massima tale che:
        # il peso degli archi sia strettamente crescente.

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo2(self, year):
        self._grafo2.clear()
        self._nodi = DAO.getAllNodes2(year)
        self._grafo2.add_nodes_from(self._nodi)
        for n in self._nodi:
            self._idMapAttori2[n.id] = n
        self.addEdges2(year)

    def addEdges2(self,year):
        self._archi = DAO.getAllEdges2(year, self._idMapAttori2)
        for e in self._archi:
            self._grafo2.add_edge(e.attore1, e.attore2, weight =e.peso)

    def getDettagliGrafo2(self):
        return len(self._grafo2.nodes), len(self._grafo2.edges)

    def getGradoGrafo(self):
        bestGrado = None
        somma = 0
        for n in self._grafo2.nodes:
            somma += self._grafo2.degree(n)
            if bestGrado is None or self._grafo2.degree(n) > self._grafo2.degree(bestGrado):
                bestGrado = n
        media = somma / len(self._grafo2.nodes)
        best10Tuple = []
        for e in self._archi:
            best10Tuple.append((e.attore1, e.attore2, e.peso))
        best10Tuple.sort(key= lambda x:x[2] , reverse=True)
        return media, bestGrado, best10Tuple[:10]

    def getCompConnessa(self):
        components = list(nx.connected_components(self._grafo2))
        largest = max(components, key = len)
        return len(components),largest

    def getPath2(self):
        self._bestPath2 = []
        parziale = []
        for n in self._grafo2.nodes:
            parziale.append(n)
            self._ricorsione2(parziale)
            parziale.pop()
        return self._bestPath2

    def _ricorsione2(self, parziale):
        if len(parziale) > len(self._bestPath2):
            self._bestPath2 = copy.deepcopy(parziale)

        for n in self._grafo2.neighbors(parziale[-1]):
            if len(parziale) ==1 :
                parziale.append(n)
                self._ricorsione2(parziale)
                parziale.pop()
            else:
                pesoPrec= self._grafo2[parziale[-1]][parziale[-2]]["weight"]
                if pesoPrec < self._grafo2[n][parziale[-1]]["weight"] and n not in parziale:
                    parziale.append(n)
                    self._ricorsione2(parziale)
                    parziale.pop()


    #VERSIONE 3
    #PUNTO 1
    # a)L'utente seleziona una soglia minima di rating.
    # b)Costruire un grafo orientato e pesato.
    # Vertici: film con rating superiore alla soglia.
    #Arco orientato F1 → F2 se:
    # almeno un attore compare in entrambi i film
    # anno(F1) < anno(F2)
    # Peso: differenza tra i rating dei due film.
    #c)Visualizzare:numero vertici, numero archi, numero componenti fortemente connesse,film con maggior numero di archi uscenti
    #PUNTO 2
    # a)Trovare il film raggiungibile dal maggior numero di altri film.
    # b)Ricorsivamente cercare il cammino semplice di peso totale massimo
    def getAllRatings2(self):
        return DAO.getAllratings2()

    def creaGrafo3(self, rating):
        self._grafo3.clear()
        self._nodi2 = DAO.getAllNodes3(rating)
        self._grafo3.add_nodes_from(self._nodi2)
        for n in self._nodi2:
            self._idMapFilm[n.id] = n
        self.addEdges3(rating)

    def addEdges3(self,rating):
        self._archi2 = DAO.getAllEdges3(rating, self._idMapFilm)
        for e in self._archi2:
            self._grafo3.add_edge(e.film1, e.film2, weight=e.peso)

    def getDettagliGrafo3(self):
        return len(self._grafo3.nodes), len(self._grafo3.edges)

    def getNumCompFortemConn(self):
        compConnString = list(nx.strongly_connected_components(self._grafo3))
        return len(compConnString)
    def filmMaxNumArchiUscenti(self):

        nodiTuple = []
        for n in self._nodi2:
            successors =len(list(self._grafo3.successors(n)))
            nodiTuple.append((n, len(successors)))
        nodiTuple.sort(key= lambda x:x[1], reverse=True)
        return nodiTuple[0]

    def getMaxConnectedComponent(self):
        components = list(nx.strongly_connected_components(self._grafo3))
        largest = max(components, key = len)
        return largest
    def getPath3(self):

        self._bestPath3 = []
        self._bestCost = 0
        parziale = []
        for n in self._grafo3.nodes:
            parziale.append(n)
            self._ricorsione3(parziale)
            parziale.pop()
        return self._bestPath3, self._bestCost

    def _ricorsione3(self, parziale):

        if self.getCost(parziale) > self._bestCost:
            self._bestCost = self.getCost(parziale)
            self._bestPath3 = copy.deepcopy(parziale)

        for n in self._grafo3.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione3(parziale)
                parziale.pop()

    def getCost(self,parziale):
        totCost = 0
        for i in range(1,len(parziale)):
            totCost += self._grafo3[parziale[i-1]][parziale[i]]["weight"]
        return totCost

    #VERSIONE 4
    #a)Effettuare una visita BFS a partire dal film scelto dall'utente.
    # Visualizzare: ordine di visita E distanza da ogni nodo.

    def getBFSPath(self, source):
        nodiPath = list(nx.bfs_tree(self._grafo3, source)) #[Source, B, C]
        distanze = nx.single_source_shortest_path_length(self._grafo3, source) # return un dizionario che come chiave ha il nodo e come valore la distanza del nodo da source
        #NON garantisce l'ordine di visita... -> fare una lista sui nodi del Path BFS
        distanzeMin = []
        for n in nodiPath:
            distanzeMin.append((n,distanze[n]))
        return nodiPath, distanzeMin

    #VERSIONE 5
    #a)L'utente seleziona un intervallo di rating
    # b)Costruire un grafo orientato e pesato.
    # Vertici: attori che hanno recitato in almeno un film nel range.
    # Arco A → B se:
    # A e B hanno lavorato insieme
    # età(A) > età(B)
    # Peso:numero di collaborazioni.
    # c)Visualizzare:numero vertici, numero archi, numero sorgenti, numero pozzi, attore con maggiore grado uscente
    # PUNTO 2
    # Utilizzando DFS individuare tutti i nodi raggiungibili da un attore scelto dall'utente.
    # Ricercare ricorsivamente il cammino semplice di peso massimo tale che:
    # le età siano strettamente decrescenti
    # non possano comparire due attori con la stessa nazionalità consecutivamente.

    def creaGrafo5(self, rating1, rating2):
        self._nodi5 = DAO.getAllNodes5(rating1, rating2)
        self._grafo5.add_nodes_from(self._nodi5)
        for n in self._nodi5:
            self._idMapAttori5[n.id] = n
        self._addEdges5(rating1, rating2)

    def addEdges5(self, rating1, rating2):
        #SOLUZIOEN 1
        self._edges5 = DAO.getAllEdges5(rating1, rating2, self._idMapAttori5)
        for e in self._edges5:
            self._grafo5.add_edge(e.attore1, e.attore2, weight=e.peso)

        #SOLUZIONE 2
        self._edges5V2 = DAO.getAllEdges5_V2(rating1, rating2, self._idMapAttori5)
        for e in self._edges5V2:
            if e.dataNscita1 < e.dataNscita2:
                a = e.attore1
                b = e.attore2
            else:
                a = e.attore2
                b= e.attore1
            if self._grafo5.has_edge(a,b):
                self._grafo5[a][b]["weight"] += 1
            else:
                self._grafo5.add_edge(a,b, weight= 1)

    def getDettagliGrafo5(self):
        #nodi sorgenti = hanno archi entranti = 0
        #nodi pozzo = hanno archi uscenti = 0
        numSorg = 0
        numPozzo = 0
        attoreMax = None
        for n in self._grafo5.nodes:
            gradoEntranteN = self._grafo5.in_degree(n)
            gradoUscenteN = self._grafo5.out_degree(n)
            if gradoEntranteN == 0 :
                numSorg += 1
            if gradoUscenteN == 0 :
                numPozzo += 1
            if attoreMax is None or self._grafo5.out_degree(attoreMax) < self._grafo5.out_degree(n):
                attoreMax = n
        return len(self._grafo5.nodes), len(self._grafo5.edges), numSorg, numPozzo, attoreMax



    def getPath4(self):
        self._bestPath4 = []
        self._bestCost4 = 0
        parziale = []
        for n in self._grafo5.nodes:
            parziale.append(n)
            self._ricorsione4(parziale)
            parziale.pop()
        return self._bestPath4, self._bestCost4

    def _ricorsione4(self, parziale):
        if self.getCost2(parziale) > self._bestCost4:
            self._bestCost4 = self.getCost2(parziale)
            self._bestPath4 = copy.deepcopy(parziale)

        for n in self._grafo3.neighbors(parziale[-1]):
            if n not in parziale and n.date_of_birth < parziale[-1].date_of_birth and n.nationality != parziale[-1].nationality:
                parziale.append(n)
                self._ricorsione4(parziale)
                parziale.pop()

    def getCost2(self,parziale):
        totCost = 0
        for i in range(1,len(parziale)):
            totCost += self._grafo5[parziale[i-1]][parziale[i]]["weight"]
        return totCost

    #VERSIONE 6
    #Cercare un percorso con peso totale massimo ma con al massimo K nodi

    def getPath5(self, k):
        self._bestPath5 = []
        self._bestCost5 = 0
        parziale = []
        for n in self._grafo3.nodes:
            parziale.append(n)
            self._ricorsione5(parziale, k)
            parziale.pop()
        return self._bestPath5, self._bestCost5

    def _ricorsione5(self, parziale, k):
        #COND OTTIMALITA
        if self.getCost3(parziale) > self._bestCost5:
            self._bestCost5 = self.getCost3(parziale)
            self._bestPath5 = copy.deepcopy(parziale)
        #CONDIZIONE TERMINAMAZIONE
        if len(parziale) == k:
            return

        for n in self._grafo3.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione5(parziale, k)
                parziale.pop()

    def getCost3(self,parziale):
        totCost = 0
        for i in range(1,len(parziale)):
            totCost += self._grafo3[parziale[i-1]][parziale[i]]["weight"]
        return totCost

    #VERSIONE 7
    #Cercare il percorso che massimizza il numero di nodi mantenendo il peso totale inferiore ad una soglia K
    def getPath6(self, k):
        self._bestPath6 = []
        parziale = []
        for n in self._grafo3.nodes:
            parziale.append(n)
            self._ricorsione6(parziale, k)
            parziale.pop()
        return self._bestPath6

    def _ricorsione6(self, parziale, k):

        if self.getCost4(parziale) > k:
            return
        if len(parziale) > len(self._bestPath6):
                self._bestPath6 = copy.deepcopy(parziale)


        for n in self._grafo3.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione6(parziale, k)
                parziale.pop()

    def getCost4(self,parziale):
        totCost = 0
        for i in range(1,len(parziale)):
            totCost += self._grafo3[parziale[i-1]][parziale[i]]["weight"]
        return totCost

    #VERSIONE 8
    #Variante BFS: Trovare il nodo più distante da un nodo scelto dall'utente.
    def trovaNodoPiuDistante(self, source):
        nodibfs = list(nx.bfs_tree(self._grafo3, source))
        distanze = nx.single_source_shortest_path_length(self._grafo, source)
        distanzeMin = []
        for n in nodibfs:
            distanzeMin.append((n,distanze[n]))
        distanzeMin.sort(key=lambda x: x[1], reverse=True)
        return distanzeMin[0]

    #VERSIONE 9
    #Elenco dei 10 film con grado maggiore
    def nodiConGradoMax(self):
        nodi9= list(self._grafo3.nodes)
        nodi9.sort(key=lambda x: self._grafo.degree(x), reverse=True)
        return self._nodi9[:10]


    #VERSIONE 10
    #Nodi = Registi
    # Arco = Due registi sono collegati se hanno diretto almeno un attore in comune
    # Ricorsione:
    # Determinare un insieme di registi contenente esattamente un regista per ogni componente connessa del grafo, massimizzando la somma dei rating.


    def creaGrafo10(self, rating):
        self._nodi10 = DAO.getAllNodes10(rating)
        self._grafo10.add_nodes_from(self._nodi10)
        for n in self._nodi10:
            self._idMapRegisti[n.id] = n
        self._edges10 = DAO.getAllEdges10(rating, self._idMapRegisti)
        for e in self._edges10:
            self._grafo10.add_edge(e.regista1, e.regista2, weight= e.peso)

    def getCompConn(self):
        components = list(nx.connected_components(self._grafo10))
        tupleCardNodoMax = []
        for n in components:
            #nodoDiGrafoMax
            nodoMax = max(n, key=lambda x: self._grafo10.degree(x))
            tupleCardNodoMax.append((n,len(n),nodoMax))
        return len(self._grafo10.nodes), len(self._grafo10.edges), len(components), tupleCardNodoMax

    def getPath10(self,k):
        self._bestPath10 = []
        self._bestCost10 = 0
        parziale=[]
        indiceComp = 0
        components = list(nx.connected_components(self._grafo10))
        #SE NON CI SONO SUFFICIENTI COMP CONNESSE -> NON è POSSIBILE TROVARE UNA SOLUZIONE
        if len(components) <k:
            return None, 0
        self._ricorsione10(components, k, parziale, indiceComp)
        return self._bestPath10, self._bestCost10

    def _ricorsione10(self, components, k, parziale, indiceComp):

        if len(parziale) == k:
            if self.getTotAvg(parziale) > self._bestCost10:
                self._bestCost10 = self.getTotAvg(parziale)
                self._bestPath10 = copy.deepcopy(parziale)
            return
        if indiceComp == len(components): #INDICE arriva fino a len -1, se indice = len vuol dire INDEXERROR(supera gli el nella lista)
            return
        #se numNodi aggiunti + numComponenti rimaste < k -> anche se prendessi un nodo da ogni comp. rimansta NON arriverei a k -> return
        if len(parziale) + (len(components)-indiceComp) < k:
            return

        componente = components[indiceComp]
        for n in componente:
            parziale.append(n)
            self._ricorsione10(components, k, parziale, indiceComp+1)
            parziale.pop()
        self._ricorsione10(components, k, parziale, indiceComp+1)

    def getTotAvg(self,parziale):
        totAvg = 0
        for n in parziale:
            totAvg += n.avg_rating
        return totAvg
    #versione2. Determinare un insieme contenente ESATTAMENTE UN regista PER OGNI componente connessa -> NON CI SAREBBE STATO IL CASO DI NON SCELTA