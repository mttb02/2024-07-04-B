import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}

        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)


    def get_all_years(self):
        return DAO.get_all_years_desc()

    def get_shapes_in_year(self, anno):
        return DAO.get_shapes_in_year(anno)

    def create_graph(self, year, shape):
        self._graph.clear()

        for s in DAO.get_all_sightings():
            if (s.shape == shape) & (s.datetime.year == year):
                self._idMap[s.id] = s
                self._graph.add_node(s)

        self._nodes = self._graph.nodes

        for a in DAO.get_edges(year, shape):
            self._graph.add_edge(self._idMap[a[0]], self._idMap[a[1]])

    def get_num_of_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_of_edges(self):
        return self._graph.number_of_edges()

    def get_num_of_comp_conn(self):
        return nx.number_weakly_connected_components(self._graph)

    def get_comp_conn_max(self):
        temp_componenti = nx.weakly_connected_components(self._graph)
        temp_sorted_componenti = sorted(temp_componenti, key=lambda c: len(c), reverse=True)
        return len(temp_sorted_componenti[0]), temp_sorted_componenti[0]

    def get_path(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self._nodes:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1

        return self._score_ottimo, self._cammino_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo, senza eccedere
        il numero ammissibile di occorrenze per un dato mese
        """
        successivi = self._graph.successors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino: list[Sighting]) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score






