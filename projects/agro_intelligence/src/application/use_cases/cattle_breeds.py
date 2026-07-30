"""
Catálogo de razas bovinas: características zootécnicas generales (raza, color, tipo,
rusticidad, resistencia a garrapata, desempeño en engorde) y qué raza conviene según la
zona. No es una serie histórica ingerida — es conocimiento zootécnico general, verificado
contra fuentes especializadas (Asociación Braford Argentina, AAPRESID, produccion-animal.com.ar),
igual de citado que arrendamiento/precio de tierra en reference_values.py.

El punto central, verificado: en el NEA (Corrientes/norte de Entre Ríos) — clima
subtropical húmedo, alta presión de garrapata — las razas británicas puras (Angus,
Hereford) rinden peor que las cruzas sintéticas con cebú (Braford, Brangus). El Braford
solo representa más del 60% de los rodeos de esa región por eso mismo.
"""

from dataclasses import dataclass

RATING_ORDER = {"Baja": 1, "Media": 2, "Media-alta": 3, "Alta": 4}


@dataclass(frozen=True)
class CattleBreed:
    name: str
    breed_type: str  # Británica (Bos taurus) / Cebú (Bos indicus) / Sintética (cruza)
    color: str
    rusticity: str  # Baja / Media / Media-alta / Alta
    tick_resistance: str
    feedlot_performance: str  # ganancia diaria de peso + conversión en engorde
    meat_quality: str  # terneza / marmoleo
    recommended_provinces: list[str]
    notes: str
    source: str


CATTLE_BREEDS: list[CattleBreed] = [
    CattleBreed(
        name="Angus",
        breed_type="Británica (Bos taurus)",
        color="Negro (Aberdeen Angus) o colorado (Angus Colorado)",
        rusticity="Media",
        tick_resistance="Baja",
        feedlot_performance="Alta",
        meat_quality="Alta — muy buen marmoleo, la más valorada en el mercado",
        recommended_provinces=["Buenos Aires", "Santa Fe", "Córdoba"],
        notes=(
            "El estándar de calidad de carne en pampa húmeda. Piel fina, poca "
            "tolerancia a calor/humedad y ectoparásitos — rinde peor en el NEA."
        ),
        source="AAPRESID / Estancias Ferguson",
    ),
    CattleBreed(
        name="Hereford",
        breed_type="Británica (Bos taurus)",
        color="Colorado con cara y línea dorsal blanca",
        rusticity="Media-alta",
        tick_resistance="Baja",
        feedlot_performance="Alta",
        meat_quality="Alta",
        recommended_provinces=["Buenos Aires", "Santa Fe", "Córdoba", "Entre Ríos"],
        notes="Precoz y dócil. Igual que Angus, pierde pie frente a la garrapata del NEA.",
        source="AAPRESID / Estancias Ferguson",
    ),
    CattleBreed(
        name="Brahman",
        breed_type="Cebú (Bos indicus)",
        color="Gris claro a blanco, papada y giba características",
        rusticity="Alta",
        tick_resistance="Alta",
        feedlot_performance="Media",
        meat_quality="Media — carne más dura, menor marmoleo que las británicas",
        recommended_provinces=["Corrientes"],
        notes=(
            "La base cebú de las cruzas sintéticas (Braford, Brangus). Solo, rinde "
            "carne de menor calidad — se usa sobre todo para cruzar, no puro."
        ),
        source="produccion-animal.com.ar",
    ),
    CattleBreed(
        name="Braford",
        breed_type="Sintética (Hereford x Brahman)",
        color="Colorado con cara blanca (hereda el patrón Hereford)",
        rusticity="Alta",
        tick_resistance="Media-alta",
        feedlot_performance="Media-alta",
        meat_quality="Media-alta — buen equilibrio con la mansedumbre del Hereford",
        recommended_provinces=["Corrientes", "Entre Ríos"],
        notes=(
            "Más del 60% de los rodeos del NEA son Braford — resistencia a garrapata y "
            "humedad muy superior a las razas británicas puras, en esteros/monte chaqueño."
        ),
        source="Asociación Braford Argentina",
    ),
    CattleBreed(
        name="Brangus",
        breed_type="Sintética (Angus x Brahman)",
        color="Negro o colorado",
        rusticity="Alta",
        tick_resistance="Media-alta",
        feedlot_performance="Media-alta",
        meat_quality="Media-alta",
        recommended_provinces=["Corrientes", "Entre Ríos"],
        notes="Algo más rústica que el Braford, aunque este último es más manso.",
        source="AAPRESID",
    ),
    CattleBreed(
        name="Limousin",
        breed_type="Continental francesa (Bos taurus)",
        color="Dorado / trigueño",
        rusticity="Media",
        tick_resistance="Baja",
        feedlot_performance="Alta",
        meat_quality="Alta — carne muy magra, buen rendimiento en res",
        recommended_provinces=["Buenos Aires", "Santa Fe"],
        notes="Se usa sobre todo como padrillo terminal en cruzas, en pampa húmeda.",
        source="produccion-animal.com.ar",
    ),
]


def recommended_breeds_for(province: str) -> list[CattleBreed]:
    return [breed for breed in CATTLE_BREEDS if province in breed.recommended_provinces]
