import datetime
from dataclasses import dataclass

from model.attore import Attore


@dataclass
class Arco5:
    attore1: Attore
    attore2: Attore
    dataNascita1 : datetime
    dataNascita2 : datetime