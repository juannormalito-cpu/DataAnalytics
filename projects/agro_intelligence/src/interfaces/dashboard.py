"""
Dashboard Streamlit: cliente delgado de application/ e infrastructure/, sin lógica de
negocio propia. Se corre con:

    streamlit run src/interfaces/dashboard.py
"""

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.correlation import correlate, correlation_matrix, to_annual_series
from src.application.use_cases.narrative import describe_series
from src.application.use_cases.reference_values import (
    land_price_reference_for,
    rental_references_for,
)
from src.application.use_cases.statistics import describe_stats
from src.application.use_cases.yearly_comparison import compute_gross_revenue
from src.config import ROOT
from src.domain.finance import evaluate_project
from src.domain.forecasting import project_linear_trend
from src.domain.taxation import estimate_export_duty
from src.domain.timeseries import Observation
from src.infrastructure.extractors.georef_ar import fetch_department_centroids
from src.infrastructure.repositories.timeseries_repository import TimeSeriesRepository

st.set_page_config(page_title="Agro Intelligence", page_icon="🌾", layout="wide")

PROVINCES = ["Buenos Aires", "Santa Fe", "Entre Ríos", "Corrientes", "Córdoba"]
CROPS = ["soja", "maiz", "trigo"]
VARIABLES = {
    "Rendimiento soja (kg/ha)": ("rendimiento_soja", "kg/ha", True),
    "Rendimiento maíz (kg/ha)": ("rendimiento_maiz", "kg/ha", True),
    "Rendimiento trigo (kg/ha)": ("rendimiento_trigo", "kg/ha", True),
    "Precio internacional soja — proxy CBOT (USD/ton)": ("precio_soja_usd_ton", "USD/ton", False),
    "Precio internacional maíz — proxy CBOT (USD/ton)": ("precio_maiz_usd_ton", "USD/ton", False),
    "Precio internacional trigo — proxy CBOT (USD/ton)": (
        "precio_trigo_usd_ton", "USD/ton", False,
    ),
    "Precio urea — insumo (USD/ton)": ("precio_urea_usd_ton", "USD/ton", False),
    "Precio novillo — Mercado de Liniers ($/kg vivo)": ("precio_novillo_liniers", "$/kg", False),
    "Bosque nativo — proxy forestal (ha)": ("bosque_nativo_ha", "ha", False),
    "Tipo de cambio oficial A3500 ($/USD)": ("tipo_cambio_a3500", "$/USD", False),
    "Dólar blue — venta ($/USD)": ("dolar_blue_venta", "$/USD", False),
}

# Centroides oficiales de cada provincia (apis.datos.gob.ar/georef, servicio de
# normalización geográfica del Estado). Son constantes geográficas, no series históricas,
# por eso van hardcodeadas acá en vez de pasar por el pipeline de ingesta.
PROVINCE_CENTROIDS = {
    "Buenos Aires": (-36.6774, -60.5585),
    "Santa Fe": (-30.7088, -60.9507),
    "Entre Ríos": (-32.0589, -59.2013),
    "Corrientes": (-28.7742, -57.8011),
    "Córdoba": (-32.1448, -63.8020),
}


@st.cache_resource
def get_repository() -> TimeSeriesRepository:
    settings = load_settings(ROOT / ".env")
    engine = get_engine(settings.database_url)
    return TimeSeriesRepository(engine)


@st.cache_data(ttl=3600)
def load_observations(variable_code: str, province: str | None) -> list[Observation]:
    return get_repository().load_observations(variable_code, province)


@st.cache_data(ttl=86400)  # geodatos estáticos, no hace falta recargarlos seguido
def load_department_centroids() -> dict[str, tuple[float, float]]:
    centroids = {}
    for province in PROVINCES:
        for name, coords in fetch_department_centroids(province).items():
            centroids[f"{name}, {province}"] = coords
    return centroids


def observations_to_frame(observations: list[Observation]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"fecha": o.date, "provincia": o.province or "Nacional", "valor": o.value}
            for o in observations
        ]
    )


st.title("🌾 Agro Intelligence")
st.caption("Buenos Aires · Santa Fe · Entre Ríos · Corrientes · Córdoba")

(
    tab_series,
    tab_stats,
    tab_mapa,
    tab_apiladas,
    tab_anual,
    tab_relaciones,
    tab_asistente,
    tab_evaluador,
) = st.tabs(
    [
        "📈 Series históricas",
        "📐 Estadísticas",
        "🗺️ Mapa",
        "📚 Series apiladas",
        "📊 Comparativa anual",
        "🔗 Relaciones",
        "🤖 Asistente de zona",
        "💰 Evaluador de proyecto",
    ]
)

with tab_series:
    label = st.selectbox("Variable", list(VARIABLES.keys()))
    variable_code, unit, has_province = VARIABLES[label]

    if has_province:
        selected_provinces = st.multiselect("Provincia", PROVINCES, default=PROVINCES)
        observations: list[Observation] = [
            observation
            for province in selected_provinces
            for observation in load_observations(variable_code, province)
        ]
    else:
        observations = load_observations(variable_code, None)

    if not observations:
        st.warning(
            "No hay datos para esta selección todavía. Corré `python main.py ingest` primero."
        )
    else:
        all_dates = [observation.date for observation in observations]
        start_date, end_date = st.slider(
            "Rango de fechas",
            min_value=min(all_dates),
            max_value=max(all_dates),
            value=(min(all_dates), max(all_dates)),
        )
        filtered = [o for o in observations if start_date <= o.date <= end_date]
        data = observations_to_frame(filtered)

        show_projection = st.checkbox(
            "Mostrar proyección de tendencia (a futuro, sin leer noticias todavía)",
            value=False,
        )

        figure = px.line(data, x="fecha", y="valor", color="provincia", markers=True)

        if show_projection:
            annual = to_annual_series(filtered)
            if len(annual) >= 2:
                projection = project_linear_trend(
                    years=list(annual.index), values=list(annual.values), years_ahead=3
                )
                figure.add_trace(
                    go.Scatter(
                        x=[date(point.year, 1, 1) for point in projection],
                        y=[point.value for point in projection],
                        mode="lines+markers",
                        name="Proyección (tendencia)",
                        line={"dash": "dash", "color": "gray"},
                    )
                )
                st.caption(
                    "La línea punteada es una proyección de tendencia lineal simple, "
                    "**no** un dato oficial ni un pronóstico riguroso."
                )

        figure.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
        st.plotly_chart(figure, use_container_width=True)

        st.info(describe_series(filtered, label=label, unit=unit))

        st.dataframe(
            data.sort_values("fecha", ascending=False), use_container_width=True, hide_index=True
        )

with tab_stats:
    st.subheader("Estadísticas descriptivas")

    label_stats = st.selectbox("Variable", list(VARIABLES.keys()), key="stats_variable")
    code_stats, unit_stats, has_province_stats = VARIABLES[label_stats]

    if has_province_stats:
        province_stats = st.selectbox(
            "Provincia (o todas)", ["Todas"] + PROVINCES, key="stats_province"
        )
        observations_stats = (
            [
                observation
                for province in PROVINCES
                for observation in load_observations(code_stats, province)
            ]
            if province_stats == "Todas"
            else load_observations(code_stats, province_stats)
        )
    else:
        observations_stats = load_observations(code_stats, None)

    stats = describe_stats(observations_stats)

    if stats is None:
        st.warning("No hay datos para esta selección todavía.")
    else:
        col_1, col_2, col_3, col_4 = st.columns(4)
        col_1.metric("Promedio", f"{stats.mean:,.1f} {unit_stats}")
        col_2.metric("Mediana", f"{stats.median:,.1f} {unit_stats}")
        col_3.metric("Mínimo", f"{stats.minimum:,.1f} {unit_stats}")
        col_4.metric("Máximo", f"{stats.maximum:,.1f} {unit_stats}")

        col_5, col_6 = st.columns(2)
        col_5.metric("Desvío estándar", f"{stats.std_dev:,.1f} {unit_stats}")
        col_6.metric(
            "Coeficiente de variación",
            f"{stats.coefficient_of_variation:.1f}%"
            if stats.coefficient_of_variation is not None
            else "N/A",
            help="Desvío estándar / promedio. Más alto = más volátil, más impredecible.",
        )

        histogram = px.histogram(
            observations_to_frame(observations_stats), x="valor", nbins=30, marginal="box"
        )
        histogram.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
        st.plotly_chart(histogram, use_container_width=True)

with tab_mapa:
    st.subheader("Vista geográfica")

    zoom_level = st.radio(
        "Nivel de zonificación",
        ["Departamento (mayor detalle)", "Provincia"],
        horizontal=True,
        key="map_zoom_level",
    )
    label_map = st.selectbox(
        "Variable",
        [key for key, value in VARIABLES.items() if value[2]],
        key="map_variable",
    )
    code_map, unit_map, _ = VARIABLES[label_map]

    st.caption(
        f"🎨 **Color y tamaño del punto** = promedio histórico de *{label_map}* en esa zona "
        f"({unit_map}). Verde más oscuro / punto más grande = valor más alto. Pasá el mouse "
        "sobre un punto para ver el nombre y el valor exacto."
    )

    if zoom_level.startswith("Departamento"):
        depto_code = f"{code_map}_depto"
        depto_observations = load_observations(depto_code, None)

        values_by_zone: dict[str, list[float]] = {}
        for observation in depto_observations:
            values_by_zone.setdefault(observation.province, []).append(observation.value)
        averages = {zone: sum(values) / len(values) for zone, values in values_by_zone.items()}

        centroids = load_department_centroids()
        map_rows = [
            {
                "zona": zone,
                "lat": centroids[zone][0],
                "lon": centroids[zone][1],
                "valor": average,
            }
            for zone, average in averages.items()
            if zone in centroids
        ]
        unmatched = len(averages) - len(map_rows)
        if unmatched:
            st.caption(
                f"({unmatched} de {len(averages)} departamentos no se pudieron ubicar en el "
                "mapa — el nombre no coincide exactamente entre la fuente de rendimientos y "
                "la de geodatos oficiales.)"
            )
    else:
        map_rows = []
        for province in PROVINCES:
            stats_province = describe_stats(load_observations(code_map, province))
            if stats_province is not None:
                lat, lon = PROVINCE_CENTROIDS[province]
                map_rows.append(
                    {"zona": province, "lat": lat, "lon": lon, "valor": stats_province.mean}
                )

    if not map_rows:
        st.warning("No hay datos para esta variable todavía.")
    else:
        map_frame = pd.DataFrame(map_rows)
        geo_map = px.scatter_geo(
            map_frame,
            lat="lat",
            lon="lon",
            size="valor",
            color="valor",
            hover_name="zona",
            color_continuous_scale="YlGn",
            scope="south america",
            labels={"valor": f"{label_map} ({unit_map})"},
        )
        geo_map.update_geos(
            center={"lat": -32, "lon": -60}, projection_scale=6, showcountries=True
        )
        geo_map.update_layout(
            margin={"l": 0, "r": 0, "t": 10, "b": 0},
            coloraxis_colorbar={"title": unit_map},
        )
        st.plotly_chart(geo_map, use_container_width=True)

        ranked = map_frame.sort_values("valor", ascending=False)
        top = ranked.head(3)
        bottom = ranked.tail(3)
        col_top, col_bottom = st.columns(2)
        with col_top:
            st.markdown("**🟢 Top 3 (mayor valor)**")
            for _, row in top.iterrows():
                st.write(f"{row['zona']}: {row['valor']:,.1f} {unit_map}")
        with col_bottom:
            st.markdown("**🔴 Últimos 3 (menor valor)**")
            for _, row in bottom.iterrows():
                st.write(f"{row['zona']}: {row['valor']:,.1f} {unit_map}")

with tab_apiladas:
    st.subheader("Series apiladas (índice base 100)")
    st.caption(
        "Cada serie se normaliza a 100 en su primer año en común, para poder apilarlas "
        "aunque las unidades originales sean distintas (kg/ha, USD/ton, $/USD, etc.). Sirve "
        "para ver cuál se movió más rápido en términos relativos, no en valores absolutos."
    )

    stacked_labels = st.multiselect(
        "Variables a apilar (elegí 2 o más)",
        list(VARIABLES.keys()),
        default=[
            "Rendimiento soja (kg/ha)",
            "Precio internacional soja — proxy CBOT (USD/ton)",
            "Dólar blue — venta ($/USD)",
        ],
        key="stacked_variables",
    )

    if len(stacked_labels) < 2:
        st.warning("Elegí al menos 2 variables para apilar.")
    else:
        annual_series = {
            label: to_annual_series(load_observations(VARIABLES[label][0], None))
            for label in stacked_labels
        }
        combined = pd.concat(annual_series, axis=1, join="inner")

        if combined.empty or len(combined) < 2:
            st.warning("No hay años en común entre todas las variables elegidas.")
        else:
            indexed = combined.div(combined.iloc[0]) * 100
            indexed.index.name = "año"
            long_format = indexed.reset_index().melt(
                id_vars="año", var_name="variable", value_name="índice (base 100)"
            )

            stacked = px.area(
                long_format, x="año", y="índice (base 100)", color="variable", markers=True
            )
            stacked.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
            st.plotly_chart(stacked, use_container_width=True)

with tab_anual:
    st.subheader("¿Qué cultivo convino más cada campaña?")
    st.caption(
        "Ingreso bruto en USD/ha = rendimiento x precio internacional de referencia "
        "(proxy CBOT — Argentina no publica precio FAS en serie abierta, ver README). "
        "Es **ingreso**, no margen neto: todavía no hay una serie completa de costo de "
        "producción para descontar, solo el precio de urea como referencia parcial."
    )

    yields_by_crop = {crop: load_observations(f"rendimiento_{crop}", None) for crop in CROPS}
    prices_by_crop = {
        crop: load_observations(f"precio_{crop}_usd_ton", None) for crop in CROPS
    }
    revenues = compute_gross_revenue(yields_by_crop, prices_by_crop)

    if not revenues:
        st.warning(
            "No hay años con rendimiento y precio disponibles al mismo tiempo todavía. "
            "Corré `python main.py ingest` primero."
        )
    else:
        revenue_frame = pd.DataFrame(
            [
                {"cultivo": r.crop, "año": r.year, "ingreso bruto (USD/ha)": r.revenue_usd_per_ha}
                for r in revenues
            ]
        )
        pivot = revenue_frame.pivot(index="cultivo", columns="año", values="ingreso bruto (USD/ha)")

        heatmap = px.imshow(
            pivot,
            color_continuous_scale="RdYlGn",
            aspect="auto",
            labels={"color": "USD/ha"},
        )
        heatmap.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
        st.plotly_chart(heatmap, use_container_width=True)

        best_row = revenue_frame.loc[revenue_frame["ingreso bruto (USD/ha)"].idxmax()]
        st.info(
            f"La mejor campaña del período fue **{best_row['cultivo']}** en "
            f"**{int(best_row['año'])}**, con **${best_row['ingreso bruto (USD/ha)']:,.0f} "
            f"USD/ha** de ingreso bruto estimado."
        )

with tab_relaciones:
    st.subheader("Matriz de correlación")
    st.caption(
        "Correlación de a pares entre todas las variables (cada par usa sus propios años "
        "en común). Sirve para detectar relaciones que no se te hubiesen ocurrido cruzar."
    )

    all_observations = {
        label: load_observations(code, None) for label, (code, _, _) in VARIABLES.items()
    }
    matrix = correlation_matrix(all_observations)

    matrix_heatmap = px.imshow(
        matrix,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto",
        labels={"color": "correlación"},
    )
    matrix_heatmap.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
    st.plotly_chart(matrix_heatmap, use_container_width=True)

    st.divider()
    st.subheader("Cruce entre dos variables")
    st.caption("Compara el promedio anual de dos variables y calcula su correlación.")

    variable_labels = list(VARIABLES.keys())
    default_a = variable_labels.index("Rendimiento soja (kg/ha)")
    default_b = variable_labels.index("Precio internacional soja — proxy CBOT (USD/ton)")

    col_a, col_b = st.columns(2)
    with col_a:
        label_a = st.selectbox("Variable A", variable_labels, index=default_a, key="var_a")
    with col_b:
        label_b = st.selectbox("Variable B", variable_labels, index=default_b, key="var_b")

    code_a, unit_a, _ = VARIABLES[label_a]
    code_b, unit_b, _ = VARIABLES[label_b]

    observations_a = load_observations(code_a, None)
    observations_b = load_observations(code_b, None)

    correlation = correlate(observations_a, observations_b)

    if correlation is None:
        st.warning("No hay suficientes años en común entre estas dos variables todavía.")
    else:
        annual_a = to_annual_series(observations_a).rename(label_a)
        annual_b = to_annual_series(observations_b).rename(label_b)
        merged = pd.concat([annual_a, annual_b], axis=1, join="inner").reset_index(names="año")

        scatter = px.scatter(merged, x=label_a, y=label_b, text="año")
        scatter.update_traces(textposition="top center")
        scatter.update_layout(margin={"l": 0, "r": 0, "t": 10, "b": 0})
        st.plotly_chart(scatter, use_container_width=True)

        abs_correlation = abs(correlation)
        if abs_correlation > 0.7:
            strength = "fuerte"
        elif abs_correlation > 0.4:
            strength = "moderada"
        else:
            strength = "débil"
        direction = "positiva" if correlation > 0 else "negativa"
        st.info(
            f"Correlación de {correlation:.2f} entre **{label_a}** y **{label_b}** "
            f"({strength}, {direction}) sobre {len(merged)} años en común."
        )

with tab_asistente:
    st.subheader("🤖 Asistente de zona")
    st.caption(
        "Rinde de referencia (dato real, ingerido), arrendamiento y precio de tierra "
        "(valores puntuales citados, no series oficiales), y una estimación de retenciones. "
        "No es asesoramiento profesional — para una decisión real, confirmá estos valores "
        "con la fuente citada y un contador para la parte impositiva."
    )

    col_zone, col_crop = st.columns(2)
    with col_zone:
        asistente_province = st.selectbox("Provincia", PROVINCES, key="asistente_province")
    with col_crop:
        asistente_crop = st.selectbox("Cultivo", CROPS, key="asistente_crop")

    yield_stats = describe_stats(
        load_observations(f"rendimiento_{asistente_crop}", asistente_province)
    )
    price_stats = describe_stats(load_observations(f"precio_{asistente_crop}_usd_ton", None))

    st.markdown("#### 📊 Rinde de referencia — dato real (MAGyP)")
    if yield_stats:
        st.metric("Rinde promedio histórico", f"{yield_stats.mean:,.0f} kg/ha")
        st.caption(f"Basado en {yield_stats.count} campañas ingeridas.")
    else:
        st.warning("Sin datos de rinde para esta combinación.")

    st.markdown("#### 🌾 Arrendamiento de referencia — valor puntual citado")
    rentals = rental_references_for(asistente_province)
    st.dataframe(
        pd.DataFrame(
            [
                {"zona": r.zone, "qq/ha": r.quintales_per_ha, "campaña": r.campaign}
                for r in rentals
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Fuente: {rentals[0].source}. Una campaña puntual, no una serie histórica.")

    st.markdown("#### 🏞️ Precio de tierra de referencia — valor puntual citado")
    land_price = land_price_reference_for(asistente_province)
    if land_price:
        st.metric(
            "Rango de referencia",
            f"USD {land_price.usd_per_ha_low:,.0f} – {land_price.usd_per_ha_high:,.0f} /ha",
        )
        st.caption(f"Fuente: {land_price.source}. Rango periodístico, no un índice oficial.")
    else:
        st.info(f"No encontré un rango de referencia citable para {asistente_province} todavía.")

    st.markdown("#### 💸 Estimación de retenciones (Decreto 423/2026)")
    if yield_stats and price_stats:
        gross_revenue = (yield_stats.mean / 1000) * price_stats.mean
        tax_estimate = estimate_export_duty(asistente_crop, gross_revenue)

        m1, m2, m3 = st.columns(3)
        m1.metric("Ingreso bruto estimado", f"${tax_estimate.gross_revenue_usd_per_ha:,.0f}/ha")
        m2.metric(
            f"Retenciones ({tax_estimate.export_duty_rate:.1%})",
            f"${tax_estimate.export_duty_usd_per_ha:,.0f}/ha",
        )
        m3.metric(
            "Neto de retenciones", f"${tax_estimate.net_of_export_duty_usd_per_ha:,.0f}/ha"
        )
        st.caption(
            "Solo derechos de exportación. Ganancias, Ingresos Brutos e Impuesto "
            "Inmobiliario Rural varían por provincia y situación fiscal particular — "
            "consultá a un contador para esos componentes."
        )
    else:
        st.warning("Faltan datos de rinde o precio internacional para estimar esto.")

with tab_evaluador:
    st.subheader("Evaluación financiera de un proyecto")
    st.caption(
        "VAN, TIR, payback e índice de rentabilidad — vale para un proyecto agrícola, "
        "ganadero o forestal: lo único que cambia es cómo armás el flujo de fondos."
    )

    left, right = st.columns([1, 2])

    with left:
        initial_investment = st.number_input(
            "Inversión inicial ($)", min_value=0.0, value=100_000.0, step=10_000.0
        )
        discount_rate = st.slider("Tasa de descuento anual", 0.0, 0.40, 0.12, 0.01)
        years = st.number_input("Años del flujo", min_value=1, max_value=15, value=5, step=1)

    with right:
        st.write("Flujo de fondos anual esperado (a partir del año 1):")
        cash_flow_inputs = [
            st.number_input(f"Año {year + 1}", value=30_000.0, step=5_000.0, key=f"cf_{year}")
            for year in range(int(years))
        ]

    cash_flows = [-abs(initial_investment), *cash_flow_inputs]
    result = evaluate_project(cash_flows, discount_rate)

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("VAN", f"${result.net_present_value:,.0f}")
    metric_2.metric(
        "TIR",
        f"{result.internal_rate_of_return:.1%}" if result.internal_rate_of_return else "N/A",
    )
    metric_3.metric(
        "Payback",
        f"{result.payback_period_years:.1f} años" if result.payback_period_years else "N/A",
    )
    metric_4.metric(
        "Índice de rentabilidad",
        f"{result.profitability_index:.2f}" if result.profitability_index else "N/A",
    )
