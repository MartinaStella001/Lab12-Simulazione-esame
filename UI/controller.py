import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenere = None
        self._choiceAttore= None

    def fillDDsGenre(self):
        generi = self._model.getAllGeneri()
        for g in generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data=g, text=g, on_click=self._saveChoiceGenere)
            )
        self._view.update_page()

    def _saveChoiceGenere(self,e):
        self._choiceGenere = e.control.data
        print(f"genere: {self._choiceGenere}")

    def handleCreaGrafo(self, e):
        if self._choiceGenere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare un genere dal menu", color="red")
            )
            self._view.update_page()
            return
        self._model.creaGrafo(self._choiceGenere)
        nodi, archi = self._model.getDettagliGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato.",color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nodi}", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {archi}", color="green")
        )
        attoreInfl = self._model.getAttorePiuInfluente()
        self._view.txt_result.controls.append(
            ft.Text(f"L'attore piu influente è {attoreInfl[0]} con influenza pari a {attoreInfl[1]}.", color="green")
        )
        self._view.update_page()
        top10attori = self._model.get10Attori()
        self._view.txt_result.controls.append(
            ft.Text(f"Top 10 attori con out-degree maggiore.", color="green")
        )
        counter = 1
        for n in top10attori:
            self._view.txt_result.controls.append(
                ft.Text(f"{counter}. {n[0]} - degree:{n[1]}")
            )
            counter += 1
        self._fillDDAttori()
        self._view.update_page()

    def _fillDDAttori(self):
        attori = self._model.getAllAttori()
        for a in attori:
            self._view._ddAttore.options.append(
                ft.dropdown.Option(data=a, text=a, on_click=self._saveChoiceAttore)
            )
        self._view.update_page()

    def _saveChoiceAttore(self,e):
        self._choiceAttore = e.control.data
        print(f"attore: {self._choiceAttore}")

    def handleCammino(self, e):
        if self._choiceAttore is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare un attore dal menu", color="red")
            )
            self._view.update_page()
            return
        #controllo dell'int N
        bestPath, bestCost = self._model.getPath(self._choiceAttore, 3)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Best path: {bestCost}", color="green")
        )
        for n in bestPath:
            self._view.txt_result.controls.append(
                ft.Text(f"{n}")
            )
        self._view.update_page()