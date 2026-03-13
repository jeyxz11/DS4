
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from .data import load_csv_to_dict, write_dict_to_csv
from .models import Animal


class Zoologico:
    DATA_DIR = Path(__file__).resolve().parent
    CLASES_FILE = DATA_DIR / "clases.csv"
    ZOO_FILE = DATA_DIR / "zoo.csv"

    def __init__(self):
        self.clases: Dict[str, str] = {}
        self.animales: Dict[str, Animal] = {}
        self.load_data()

    def load_data(self) -> None:
        clases_raw = load_csv_to_dict(self.CLASES_FILE, key_field="Clase_tipo")
        if not clases_raw:
            clases_raw = load_csv_to_dict(self.CLASES_FILE, key_field="clase")

        self.clases = {
            k: v.get("descripcion", v.get("Clase_id", "")) for k, v in clases_raw.items()
        }

        animales_raw = load_csv_to_dict(self.ZOO_FILE, key_field="nombre_animal")
        if not animales_raw:
            animales_raw = load_csv_to_dict(self.ZOO_FILE, key_field="nombre")

        self.animales = {
            nombre: Animal.from_dict(row)
            for nombre, row in animales_raw.items()
            if nombre
        }

    def save_animals(self) -> None:
        fieldnames = ["nombre", "clase", "caracteristicas"]
        data = {name: animal.to_dict() for name, animal in self.animales.items()}
        write_dict_to_csv(self.ZOO_FILE, data, fieldnames, sort_keys=True)

    def listar_por_clase(self, clase: str) -> List[Animal]:
        clase = clase.strip()
        return [a for a in self.animales.values() if a.clase.lower() == clase.lower()]

    def listar_por_caracteristica(self, caracteristica: str) -> List[Animal]:
        caracteristica = caracteristica.strip().lower()
        return [
            a
            for a in self.animales.values()
            if any(caracteristica in c.lower() for c in a.caracteristicas)
        ]

    def agregar_animal(
        self,
        nombre: str,
        clase: str,
        caracteristicas: List[str],
        persist: bool = False,
    ) -> Optional[Animal]:


        nombre = nombre.strip()
        if not nombre:
            return None

        if nombre in self.animales:
            return None

        clase = clase.strip()
        if clase and clase not in self.clases:
            
            self.clases[clase] = ""

        animal = Animal(nombre=nombre, clase=clase, caracteristicas=caracteristicas)
        self.animales[nombre] = animal

        if persist:
            self.save_animals()

        return animal

    def obtener_clases(self) -> List[str]:
        return sorted(self.clases.keys())

    def obtener_caracteristicas(self) -> List[str]:
        características = set()
        for animal in self.animales.values():
            características.update([c.strip() for c in animal.caracteristicas if c.strip()])
        return sorted(características)
