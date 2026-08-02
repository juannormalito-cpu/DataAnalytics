"""Builds the portfolio landing page, embedding selected charts as base64
so the resulting HTML is fully self-contained (no external requests)."""

import base64
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\facus\DataAnalytics\scratch_ml_pdf")
from diagrams_svg import ALL_DIAGRAMS  # noqa: E402

REPORTS = Path(r"C:\Users\facus\DataAnalytics\projects\fintech_fraud_intelligence\reports")
OUT = Path(__file__).resolve().parent


def img_b64(name: str) -> str:
    data = (REPORTS / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


IMAGES = {
    "TENDENCIA": img_b64("tendencia_diaria.png"),
    "FRAUDE_TIPO": img_b64("tasa_fraude_por_tipo.png"),
    "CURVAS": img_b64("modelo_fraude_curvas.png"),
    "IMPORTANCIA": img_b64("importancia_features.png"),
    "SHAP": img_b64("shap_summary.png"),
    "ALGORITMOS": img_b64("comparacion_algoritmos.png"),
}

TEMPLATE = Path(__file__).with_name("template.html").read_text(encoding="utf-8")

html = TEMPLATE
for key, data_uri in IMAGES.items():
    html = html.replace(f"__IMG_{key}__", data_uri)

html = html.replace("__DIAGRAM_OVERVIEW__", ALL_DIAGRAMS["overview"])
html = html.replace("__DIAGRAM_LOCAL__", ALL_DIAGRAMS["local_vs_autonomo"])

(OUT / "index.html").write_text(html, encoding="utf-8")
print("index.html generado")
