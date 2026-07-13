

from dataclasses import dataclass

from model.film import Film


@dataclass
class Arco3:
    film1 : Film
    film2 : Film
    peso: int