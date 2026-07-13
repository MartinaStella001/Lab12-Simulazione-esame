from dataclasses import dataclass

from model.regista import Regista

@dataclass
class Arco:
    regista1 : Regista
    regista2 : Regista
    numFilmGenereComune: int