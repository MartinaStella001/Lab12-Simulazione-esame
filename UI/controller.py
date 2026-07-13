import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAvg1 = None
        self._choiceAvg2 = None

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        for r in ratings:
            self._view._ddrating1.options.append(
                ft.dropdown.Option(data=r, key=r, on_click=self.saveDD1)
            )
            self._view._ddrating2.options.append(
                ft.dropdown.Option(data=r, key=r, on_click=self.saveDD2))

        self._view.update_page()

    def saveDD1(self,e):
        self._choiceAvg1 = e.control.data
        print(f"Voto 1: {self._choiceAvg1}")

    def saveDD2(self, e):
        self._choiceAvg2 = e.control.data
        print(f"Voto 2: {self._choiceAvg2}")


    def handleCreaGrafo(self, e):
        if self._choiceAvg1 is None or self._choiceAvg2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un valore dal menu", color="red")
            )
        self._model.creaGrafo(self._choiceAvg1, self._choiceAvg2)
        nodi, archi = self._model.getDettagliGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente:", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {nodi}", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {archi}", color="green")
        )
        best5 = self._model.best5Archi()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Top 5 archi:", color="green")
        )
        for e in best5:
            self._view.txt_result.controls.append(
                ft.Text(f"{e[0]} -> {e[1]} : {e[2]}")
            )
        lun, bestComp = self._model.getCompConnesse()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {lun} componenti connesse", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"la più grande componente connessa è lunga {len(bestComp)} ", color="green")
        )
        for e in bestComp:
            self._view.txt_result.controls.append(
                ft.Text(e)
            )
        self._view.update_page()

    def handleCammino(self, e):
        bestPath = self._model.getPath()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato miglior cammino di lunghezza {len(bestPath)}.Di seguito i nodi che lo compongono", color="green")
        )
        for n in bestPath:
            self._view.txt_result.controls.append(
            ft.Text(n)
        )
        self._view.update_page()