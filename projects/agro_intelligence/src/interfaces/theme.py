"""
Sistema de diseño del dashboard: una paleta validada (CVD-safe, contraste verificado)
aplicada consistentemente en todos los gráficos, en vez de que cada `px.line`/`px.imshow`
elija colores por su cuenta (lo que hacía que, por ejemplo, "Buenos Aires" fuera un color
distinto en cada pestaña).

- Categórica: color fijo por entidad (provincia/cultivo), mismo orden siempre.
- Secuencial: un solo tono (azul), para magnitud (mapas, heatmaps de valores).
- Divergente: azul↔gris↔rojo, para polaridad (matriz de correlación).

No se inventaron estos valores: son la paleta de referencia validada (CVD ΔE ≥ 8,
contraste ≥ 3:1) del skill de dataviz del equipo.
"""

# Orden fijo de 8 tonos categóricos — nunca ciclar, nunca reasignar por ranking.
CATEGORICAL_SEQUENCE = [
    "#2a78d6",  # 1 azul
    "#eb6834",  # 2 naranja
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 amarillo
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 verde
    "#4a3aa7",  # 7 violeta
    "#e34948",  # 8 rojo
]

# Provincia -> color fijo, igual en todas las pestañas.
PROVINCE_COLORS = {
    "Buenos Aires": CATEGORICAL_SEQUENCE[0],
    "Córdoba": CATEGORICAL_SEQUENCE[1],
    "Santa Fe": CATEGORICAL_SEQUENCE[2],
    "Entre Ríos": CATEGORICAL_SEQUENCE[3],
    "Corrientes": CATEGORICAL_SEQUENCE[4],
    "Nacional": "#898781",  # ink muted, no es una provincia
}

# Cultivo -> color fijo. Solo 3 (soja/maíz/trigo): quedan dentro de los primeros 3 slots,
# los únicos que validan CVD incluso en contextos "todos contra todos" (scatter/heatmap).
CROP_COLORS = {
    "soja": CATEGORICAL_SEQUENCE[0],
    "maiz": CATEGORICAL_SEQUENCE[1],
    "trigo": CATEGORICAL_SEQUENCE[2],
}

# Secuencial: un solo tono (azul), claro -> oscuro, para magnitud (mapas, heatmaps).
SEQUENTIAL_BLUE = [
    "#cde2fb",
    "#9ec5f4",
    "#6da7ec",
    "#3987e5",
    "#256abf",
    "#1c5cab",
    "#104281",
    "#0d366b",
]

# Divergente: azul <-> gris neutro <-> rojo, para polaridad (correlación, -1 a 1).
DIVERGING_BLUE_RED = [
    [0.0, "#0d366b"],
    [0.25, "#3987e5"],
    [0.5, "#f0efec"],
    [0.75, "#eb6864"],
    [1.0, "#8a2020"],
]

CHART_SURFACE = "#fcfcfb"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
AXIS_LINE = "#c3c2b7"

FONT_FAMILY = "system-ui, -apple-system, 'Segoe UI', sans-serif"


def style_figure(figure):
    """Aplica tipografía, grillas y superficie consistentes a cualquier figura Plotly."""
    figure.update_layout(
        font={"family": FONT_FAMILY, "color": PRIMARY_INK, "size": 13},
        paper_bgcolor=CHART_SURFACE,
        plot_bgcolor=CHART_SURFACE,
        legend={"font": {"color": SECONDARY_INK}},
        hoverlabel={"font": {"family": FONT_FAMILY}},
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
    )
    figure.update_xaxes(
        gridcolor=GRIDLINE, linecolor=AXIS_LINE, tickfont={"color": MUTED_INK}, zeroline=False
    )
    figure.update_yaxes(
        gridcolor=GRIDLINE, linecolor=AXIS_LINE, tickfont={"color": MUTED_INK}, zeroline=False
    )
    return figure


def color_for_province(province: str | None) -> str:
    return PROVINCE_COLORS.get(province or "Nacional", MUTED_INK)


def color_for_crop(crop: str) -> str:
    return CROP_COLORS.get(crop, MUTED_INK)
