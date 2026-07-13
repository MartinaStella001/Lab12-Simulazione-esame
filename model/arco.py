from dataclasses import dataclass

from model.film import Film


@dataclass
class Arco:
    film1: Film
    film2: Film
    numGeneriComune: int
    numAttoriComuni: int