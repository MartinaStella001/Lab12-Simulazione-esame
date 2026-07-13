from dataclasses import dataclass

from model.regista import Regista


@dataclass
class Arco10:
    regista1: Regista
    regista2: Regista
    peso : int