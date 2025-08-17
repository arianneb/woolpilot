from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    brand: str
    name: str
    price: Optional[float] = None
    availability: Optional[str] = None
    needle_size: Optional[str] = None
    composition: Optional[str] = None
    source_url: Optional[str] = None
