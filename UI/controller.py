import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._anno_selezionato = None
        self._forma_selezionata = None

    def handle_graph(self, e):
        if self._anno_selezionato is None:
            self._view.create_alert("Selezionare un anno")
            return
        if self._forma_selezionata is None:
            self._view.create_alert("Selezionare una forma")
            return

        self._view.txt_result1.controls.clear()

        self._model.create_graph(self._anno_selezionato, self._forma_selezionata)

        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_edges()}"))

        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {self._model.get_num_of_comp_conn()} componenti connesse"))

        num_compnenti, componente = self._model.get_comp_conn_max()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {num_compnenti} nodi:"))
        for n in componente:
            self._view.txt_result1.controls.append(
                ft.Text(f"{n}"))

        self._view.btn_path.disabled = False

        self._view.update_page()


    def handle_path(self, e):

        self._view.txt_result2.controls.clear()

        temp_punteggio, temp_avvistamenti = self._model.get_path()

        self._view.txt_result2.controls.append(ft.Text(f"Cammino con punteggio massimo: {temp_punteggio}"))
        for a in temp_avvistamenti:
            self._view.txt_result2.controls.append(
                ft.Text(f"{a}"))

        self._view.update_page()

        self._view.btn_path.disabled = True


    def populate_ddyear(self):
        self._view.ddyear.options.clear()

        temp_anni = self._model.get_all_years()

        for a in temp_anni:
            self._view.ddyear.options.append(ft.dropdown.Option(key=a, text=a, on_click=self.get_year))

        self._view.update_page()

    def get_year(self, e):
        if e.control.key is None:
            self._view.create_alert("Selezionare un anno")
        else:
            self._anno_selezionato = e.control.key
            self.populate_ddshape()
            self._view.btn_path.disabled = True

    def populate_ddshape(self):
        self._view.ddshape.options.clear()

        temp_forme = self._model.get_shapes_in_year(self._anno_selezionato)

        for f in temp_forme:
            self._view.ddshape.options.append(ft.dropdown.Option(key=f, text=f, on_click=self.get_shape))

        self._view.update_page()

    def get_shape(self, e):
        if e.control.key is None:
            self._view.create_alert("Selezionare una forma")
        else:
            self._forma_selezionata = e.control.key
            self._view.btn_path.disabled = True






