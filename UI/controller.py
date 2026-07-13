import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceYear = None

    def fillDDsYear(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddYear.options.append(
                ft.dropdown.Option(data=y, text=y, on_click=self._saveYear)
            )
        self._view.update_page()
    def _saveYear(self, e):
        self._choiceYear = e.control.data
        print(f"year: {self._choiceYear}")

    def handleCreaGrafo(self, e):
        pass

    def handleCammino(self, e):
        pass