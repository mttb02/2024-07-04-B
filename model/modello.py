from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def get_all_years(self):
        return DAO.get_all_years()

    def get_states_year(self, anno):
        return DAO.get_states_year(anno)

    def create_graph(self, year, state):

        self._graph.clear()

        for s in DAO.get_all_sightings():
            if s.datetime.year == int(year) and s.state == state.lower():
                self._idMap[s.id] = s
                self._graph.add_node(s)

        for a in DAO.get_avvistamenti(year, state):
            if (a[0] in self._idMap) & (a[1] in self._idMap):
                if self._idMap[a[0]].distance_HV(self._idMap[a[1]]) < 100:
                    self._graph.add_edge(self._idMap[a[0]], self._idMap[a[1]])

    def get_num_vertici(self):
        return len(self._graph.nodes)

    def get_num_archi(self):
        return len(self._graph.edges)

    def get_num_comp_conn(self):
        return nx.number_connected_components(self._graph)

    def get_max_comp_conn(self):
        comp_conn = nx.connected_components(self._graph)
        comp_max = (0, "")
        for c in comp_conn:
            if len(c) > comp_max[0]:
                comp_max = (len(c), c)
        return comp_max






