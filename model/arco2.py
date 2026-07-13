
from dataclasses import dataclass

from model.attore import Attore


@dataclass
class Arco2:
    attore1 : Attore
    attore2 : Attore
    peso: int