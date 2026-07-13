import datetime
from dataclasses import dataclass

from model.attore import Attore


@dataclass
class Arco:
    attore1 : Attore
    attore2 : Attore
    incasso: str