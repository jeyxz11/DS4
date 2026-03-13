
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Animal:
    
    nombre: str
    clase: str
    caracteristicas: List[str]

    def __post_init__(self):
        self.nombre = self.nombre.strip()
        self.clase = self.clase.strip()
        self.caracteristicas = [c.strip() for c in self.caracteristicas if c.strip()]

    def __str__(self) -> str:
        carac = "; ".join(self.caracteristicas)
        return f"{self.nombre} ({self.clase}) - Características: {carac}"

    def __repr__(self) -> str:
        return (
            f"Animal(nombre={self.nombre!r}, clase={self.clase!r}, "
            f"caracteristicas={self.caracteristicas!r})"
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Animal":

        nombre = (data.get("nombre") or data.get("nombre_animal") or "").strip()
        clase = (data.get("clase") or data.get("Clase_tipo") or "").strip()

        if "caracteristicas" in data and str(data.get("caracteristicas", "")).strip():
            caracteristicas_raw = str(data.get("caracteristicas", ""))
            caracteristicas = [c.strip() for c in caracteristicas_raw.split(";") if c.strip()]
        else:
            caracteristicas = []
            for key, value in data.items():
                if key in {"nombre", "nombre_animal", "clase", "Clase_tipo", "caracteristicas"}:
                    continue
                if str(value).strip().lower() in {"1", "true", "t", "yes", "y", "si"}:
                    caracteristicas.append(key)

        return cls(nombre=nombre, clase=clase, caracteristicas=caracteristicas)

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "clase": self.clase,
            "caracteristicas": ";".join(self.caracteristicas),
        }
