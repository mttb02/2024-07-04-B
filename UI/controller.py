import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def populate_ddyear(self):
        self._view.ddyear.options.clear()
        temp_years = self._model.get_all_years()

        for y in temp_years:
            self._view.ddyear.options.append(ft.dropdown.Option(key=y, text=y, on_click=self.populate_ddstate))

        self._view.update_page()

    def populate_ddstate(self, e):
        if e.control.key is None:
            self._view.create_alert("Selezionare un anno!")
            return

        self._view.ddstate.options.clear()

        for s in self._model.get_states_year(e.control.key):
            self._view.ddstate.options.append(ft.dropdown.Option(key=s.id, text=s.name))

        self._view.update_page()

    def handle_graph(self, e):

        self._view.txt_result1.controls.clear()

        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        else:
            temp_anno = self._view.ddyear.value

        if self._view.ddstate.value is None:
            self._view.create_alert("Selezionare uno stato!")
            return
        else:
            temp_stato = self._view.ddstate.value

        self._model.create_graph(temp_anno, temp_stato)

        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_vertici()}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {self._model.get_num_archi()}"))

        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {self._model.get_num_comp_conn()} componenti connesse"))

        max_comp_conn = self._model.get_max_comp_conn()

        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {max_comp_conn[0]} nodi:"))

        for c in max_comp_conn[1]:
            self._view.txt_result1.controls.append(
                ft.Text(f"{c}"))

        self._view.update_page()


    def handle_path(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        else:
            temp_anno = self._view.ddyear.value

        if self._view.ddstate.value is None:
            self._view.create_alert("Selezionare uno stato!")
            return
        else:
            temp_stato = self._view.ddstate.value







